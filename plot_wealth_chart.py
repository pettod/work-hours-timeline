import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sys


# CSV file name and delimiter in CSV file
CSV_FILE_NAME = "omaisuus.csv"
DELIMITER = ','

# Date format e.g. 31.12.2019 or 12/31/2019
# Set how often the date is shown in x-axis, can use mdates.DayLocator
DATE_FORMAT = "%Y"
LOCATOR = mdates.MonthLocator 
X_AXIS_INTERVAL = 12


def readCsvData(file_name, delimiter):
    years = []
    savings = []
    investments = []
    equities = []
    total_days = []
    with open(file_name, 'r') as csv_file:
        line_reader = csv.reader(csv_file, delimiter=delimiter)
        for i, line in enumerate(line_reader):
            if i == 0:
                continue
            day = int(line[0])
            month = int(line[1])
            year = int(line[2])
            saving = int(line[3])
            investment = int(line[4])
            years.append(year)
            savings.append(saving)
            investments.append(investment)
            equities.append(saving + investment)
            date = "{}/{}/{}".format(month, day, year)
            total_number_of_days = mdates.datestr2num(date)
            total_days.append(total_number_of_days)
    return savings, investments, equities, total_days


def plotDataPerDay(total_days, datas, labels, title, ylabel):
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(DATE_FORMAT))
    plt.gca().xaxis.set_major_locator(LOCATOR(interval=X_AXIS_INTERVAL))
    for data, label in zip(datas, labels):
        plt.plot(total_days, data, label=label)
    plt.legend()
    plt.grid(axis='y')
    plt.gcf().autofmt_xdate()
    plt.xlabel("Date")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()


def getRedGreenColorMap(data):
    color_map = []
    for value in data:
        if value < 0:
            color_map.append('r')
        else:
            color_map.append('g')
    return tuple(color_map)


def readCommandLineArguments():
    csv_file_name = CSV_FILE_NAME
    delimiter = DELIMITER
    if len(sys.argv) > 1:
        csv_file_name = sys.argv[1]
    if len(sys.argv) > 2:
        delimiter = sys.argv[2]
    return csv_file_name, delimiter


def main():
    # Read data
    csv_file_name, delimiter = readCommandLineArguments()
    (
        savings,
        investments,
        equities,
        total_days,
    ) = readCsvData(csv_file_name, delimiter)

    # Analyze data
    plotDataPerDay(
        total_days,
        [savings, investments, equities],
        ["Savings", "Stock profits", "Equity"],
        "Wealth progress", "€")


main()
