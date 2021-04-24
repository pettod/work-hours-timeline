import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sys
from math import sqrt, ceil


# CSV file name and delimiter in CSV file
CSV_FILE_NAME = "omaisuus.csv"
DELIMITER = ','

# Date format e.g. 31.12.2019 or 12/31/2019
# Set how often the date is shown in x-axis, can use mdates.DayLocator
DATE_FORMAT = "%Y"
LOCATOR = mdates.YearLocator


def readCsvData(file_name, delimiter):
    date_values = {
        "savings": [],
        "stock_profits": [],
        "equities": [],
        "dates_as_numbers": [],
    }
    year_values = {
        "savings": [],
        "stock_profits": [],
        "equities": [],
        "years": [],
    }
    previous_year = None
    with open(file_name, 'r') as csv_file:
        line_reader = csv.reader(csv_file, delimiter=delimiter)
        for i, line in enumerate(line_reader):
            if i == 0:
                continue
            [day, month, year, saving, stock_profit] = [int(l) for l in line]
            date = "{}/{}/{}".format(month, day, year)
            date_as_number = mdates.datestr2num(date)

            # Store values
            date_values["savings"].append(saving)
            date_values["stock_profits"].append(stock_profit)
            date_values["equities"].append(saving + stock_profit)
            date_values["dates_as_numbers"].append(date_as_number)

            # Interpolate values on year's last day 31st of Dec
            if previous_year is not None and year > previous_year:
                year_values["years"].append(previous_year)

                # Take x-axis values (dates)
                x0 = date_values["dates_as_numbers"][-2]
                x2 = date_as_number
                x1 = mdates.datestr2num(f"31/12/{previous_year}")

                # Interpolate y-axis values (weighted average)
                for key in date_values.keys():
                    if key == "dates_as_numbers":
                        continue
                    y0 = date_values[key][-2]
                    y2 = date_values[key][-1]
                    y1 = y0 + (y2 - y0) * (x1 - x0) / (x2 - x0)
                    year_values[key].append(y1)
            previous_year = year
    return date_values, year_values


def plotDataPerDay(dates_as_numbers, datas, labels, title, ylabel):
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(DATE_FORMAT))
    plt.gca().xaxis.set_major_locator(LOCATOR())
    for data, label in zip(datas, labels):
        plt.plot(dates_as_numbers, data, label=label)
    plt.legend()
    plt.grid(axis='y')
    plt.gcf().autofmt_xdate()
    plt.xlabel("Date")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()


def readCommandLineArguments():
    csv_file_name = CSV_FILE_NAME
    delimiter = DELIMITER
    if len(sys.argv) > 1:
        csv_file_name = sys.argv[1]
    if len(sys.argv) > 2:
        delimiter = sys.argv[2]
    return csv_file_name, delimiter


def percentageYearlyGrowth(year_values, skip_keys, equity_comparison_keys=[]):
    percentage_yearly_growth = {}

    # Growth compared to last year value
    for key in year_values.keys():
        if key in skip_keys:
            continue
        growths = []
        for i in range(1, len(year_values[key])):
            growths.append(
                100 * (year_values[key][i] / year_values[key][i-1] - 1))
        percentage_yearly_growth[key] = growths

    # Growth compared to last year equity
    for key in equity_comparison_keys:
        growths = []
        for i in range(1, len(year_values[key])):
            growth = 100 * (year_values[key][i] / year_values["equities"][i-1] - 1)
            if key == "stock_profits":
                growth += 100
            growths.append(growth)
        percentage_yearly_growth[key + "_per_equity"] = growths
    percentage_yearly_growth["years"] = year_values["years"][1:].copy()
    return percentage_yearly_growth


def getRedGreenColorMap(data):
    color_map = []
    for value in data:
        if value < 0:
            color_map.append('r')
        else:
            color_map.append('g')
    return tuple(color_map)


def plotBarChart(x, y, title, show=True):
    plt.bar(x, y, color=getRedGreenColorMap(y))
    plt.title(title)
    plt.xlabel("Year")
    plt.ylabel("%")
    if show:
        plt.show()


def main():
    # Read data
    csv_file_name, delimiter = readCommandLineArguments()
    date_values, year_values = readCsvData(csv_file_name, delimiter)
    percentage_yearly_growth = percentageYearlyGrowth(
        year_values, ["years", "stock_profits"], ["stock_profits", "savings"])

    # Plot data
    plotDataPerDay(
        date_values["dates_as_numbers"],
        [
            date_values["savings"],
            date_values["stock_profits"],
            date_values["equities"]
        ], ["Savings", "Stock profits", "Equity"],
        "Wealth progress", "€")

    # Plot growth
    y = [
        percentage_yearly_growth["stock_profits_per_equity"],
        percentage_yearly_growth["savings_per_equity"],
        percentage_yearly_growth["equities"],
        percentage_yearly_growth["savings"],
    ]
    titles = [
        "YoY Stock profit per equity",
        "YoY Savings per equity",
        "YoY Equity growth",
        "YoY Savings growth",
    ]
    grid_x = int(sqrt(len(y)))
    grid_y = ceil(len(y) / grid_x)
    for i in range(len(y)):
        plt.subplot(grid_x, grid_y, i+1)
        plotBarChart(percentage_yearly_growth["years"], y[i], titles[i], False)
    plt.show()


main()
