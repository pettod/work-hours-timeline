import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sys


# CSV file name and delimiter in CSV file
CSV_FILE_NAME = "progress.csv"
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
    progresses = []
    total_days = []
    name_of_progress = "progress"
    with open(file_name, 'r') as csv_file:
        line_reader = csv.reader(csv_file, delimiter=delimiter)
        for i, line in enumerate(line_reader):
            if i == 0:
                name_of_progress = line[4].lower()
                continue
            day = line[0]
            month = line[1]
            year = line[2]
            hour = line[3]
            progress = line[4]
            days.append(int(day))
            months.append(int(month))
            years.append(int(year))
            hours.append(int(hour))
            progresses.append(int(progress))
            date = month + '/' + day + '/' + year
            total_number_of_days = mdates.datestr2num(date)
            total_days.append(total_number_of_days)
    return days, months, hours, progresses, total_days, name_of_progress


def plotDataPerDay(total_days, data, title, ylabel):
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(DATE_FORMAT))
    plt.gca().xaxis.set_major_locator(LOCATOR(interval=X_AXIS_INTERVAL))
    plt.bar(total_days, data)
    plt.gcf().autofmt_xdate()
    plt.xlabel("Date")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()


def plot2Datasets(total_days, data_1, data_2, title, ylabel_1, ylabel_2,
                  data_name_1, data_name_2, absolute=False, bar_width=0.3):
    fig = plt.figure()
    ax_1 = fig.add_subplot(111)
    ax_2 = ax_1.twinx()

    if absolute:
        color_map = []
        for value in data_2:
            if value < 0:
                color_map.append('r')
            else:
                color_map.append('g')
        color = tuple(color_map)
        ax_2.plot(total_days, list(np.zeros(len(total_days))), color="black")
    else:
        color = "tab:orange"

    indices_1 = list(np.array(total_days) - bar_width / 2)
    indices_2 = list(np.array(total_days) + bar_width / 2)
    bar_1 = ax_1.bar(indices_1, data_1, bar_width, label=data_name_1)
    ax_1.set_ylabel(ylabel_1)
    bar_2 = ax_2.bar(
        indices_2, data_2, bar_width, label=data_name_2,
        color=color)
    ax_2.set_ylabel(ylabel_2)

    fig.legend()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(DATE_FORMAT))
    plt.gca().xaxis.set_major_locator(LOCATOR(interval=X_AXIS_INTERVAL))
    plt.gcf().autofmt_xdate()
    ax_1.set_xlabel("Date")
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


def getAbsoluteProgresses(cumulative_progresses):
    absolute_progresses = []
    for i in range(len(cumulative_progresses)):
        absolute_progress = cumulative_progresses[i]
        if i > 0:
            absolute_progress -= cumulative_progresses[i-1]
        absolute_progresses.append(absolute_progress)
    return absolute_progresses


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
    days, months, hours, cumulative_progresses, total_days, \
    name_of_progress = readCsvData(csv_file_name, delimiter)
    cumulative_hours = getCumulativeHours(hours)
    absolute_progresses = getAbsoluteProgresses(cumulative_progresses)
    print("Total working hours: %i" % (cumulative_hours[-1]))

    # Analyze data
    plotDataPerDay(total_days, hours, "Hours per day", "Hours")
    plotDataPerDay(total_days, cumulative_hours, "Cumulative hours", "Hours")
    plot2Datasets(
        total_days, hours, absolute_progresses,
        "Working hours and absolute " + name_of_progress, "Hours",
        name_of_progress.title(), "working hours",
        "absolute " + name_of_progress, absolute=True)
    plot2Datasets(
        total_days, hours, cumulative_progresses,
        "Working hours and cumulative " + name_of_progress, "Hours",
        name_of_progress.title(), "working hours",
        "cumulative " + name_of_progress)
    

main()
