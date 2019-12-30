import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sys


# CSV file name and delimiter in CSV file
CSV_FILE_NAME = "work_hours.csv"
DELIMITER = ','

# Date format e.g. 31.12.2019 or 12/31/2019
# Set how often the date is shown in x-axis, can use mdates.DayLocator
DATE_FORMAT = "%d.%m.%Y"
LOCATOR = mdates.MonthLocator 
X_AXIS_INTERVAL = 1


def readCsvData(file_name, delimiter):
    days = []
    months = []
    years = []
    hours = []
    total_days = []
    with open(file_name, 'r') as csv_file:
        line_reader = csv.reader(csv_file, delimiter=delimiter)
        for i, line in enumerate(line_reader):
            if i == 0:
                continue
            day = line[0]
            month = line[1]
            year = line[2]
            hour = line[3]
            days.append(int(day))
            months.append(int(month))
            years.append(int(year))
            hours.append(int(hour))
            date = month + '/' + day + '/' + year
            total_number_of_days = mdates.datestr2num(date)
            total_days.append(total_number_of_days)
    return days, months, hours, total_days


def plotDataPerDay(total_days, data, title, ylabel):
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(DATE_FORMAT))
    plt.gca().xaxis.set_major_locator(LOCATOR(interval=X_AXIS_INTERVAL))
    plt.bar(total_days, data)
    plt.gcf().autofmt_xdate()
    plt.xlabel("Date")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()


def getCumulativeHours(hours):
    cumulative_hours = []
    for i in range(len(hours)):
        cumulative_hour = hours[i]
        if i > 0:
            cumulative_hour += cumulative_hours[-1]
        cumulative_hours.append(cumulative_hour)
    return cumulative_hours


def readCommandLineArguments():
    csv_file_name = CSV_FILE_NAME
    delimiter = DELIMITER
    if len(sys.argv) > 1:
        csv_file_name = sys.argv[1]
    if len(sys.argv) > 2:
        delimiter = sys.argv[2]
    return csv_file_name, delimiter


def main():
    csv_file_name, delimiter = readCommandLineArguments()
    days, months, hours, total_days = readCsvData(csv_file_name, delimiter)
    plotDataPerDay(total_days, hours, "Hours per day", "Hours")
    cumulative_hours = getCumulativeHours(hours)
    plotDataPerDay(total_days, cumulative_hours, "Cumulative hours", "Hours")
    print("Total working hours: %i" % (cumulative_hours[-1]))
    

main()
