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
    name_of_progress = None
    with open(file_name, 'r') as csv_file:
        line_reader = csv.reader(csv_file, delimiter=delimiter)
        for i, line in enumerate(line_reader):
            if i == 0:
                if len(line) >= 5:
                    name_of_progress = line[4].lower()
                continue
            day = line[0]
            month = line[1]
            year = line[2]
            days.append(int(day))
            months.append(int(month))
            years.append(int(year))
            hours.append(float(line[3]))
            if len(line) >= 5:
                progresses.append(float(line[4]))
            date = month + '/' + day + '/' + year
            total_number_of_days = mdates.datestr2num(date)
            total_days.append(total_number_of_days)
    return days, months, hours, progresses, total_days, name_of_progress


def plotDataPerDay(total_days, data, title, ylabel,
                   values_can_be_negative=False):
    color = "C0"
    if values_can_be_negative:
        color = getRedGreenColorMap(data)
        plt.plot(total_days, list(np.zeros(len(total_days))), color="black")
        data_array = np.array(data)
        indices_of_nonzeros = np.where(data_array != 0.0)[0]
        filtered_total_days = list(np.delete(
            np.array(total_days), indices_of_nonzeros))
        filtered_data = list(data_array[data_array == 0.0])
        plt.plot(filtered_total_days, filtered_data, "ro")

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(DATE_FORMAT))
    plt.gca().xaxis.set_major_locator(LOCATOR(interval=X_AXIS_INTERVAL))
    plt.bar(total_days, data, color=color)
    plt.gcf().autofmt_xdate()
    plt.xlabel("Date")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()


def plot2Datasets(total_days, data_1, data_2, title, ylabel_1, ylabel_2,
                  data_name_1, data_name_2, values_can_be_negative=False,
                  bar_width=0.3):
    fig = plt.figure()
    ax_1 = fig.add_subplot(111)
    ax_2 = ax_1.twinx()

    color = "tab:orange"
    if values_can_be_negative:
        color = getRedGreenColorMap(data_2)
        ax_2.plot(total_days, list(np.zeros(len(total_days))), color="black")

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


def getRedGreenColorMap(data):
    color_map = []
    for value in data:
        if value < 0:
            color_map.append('r')
        else:
            color_map.append('g')
    return tuple(color_map)


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


def getAbsoluteProgressPerHours(absolute_progresses, hours):
    return list(np.array(absolute_progresses) / np.array(hours))


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
    print("Total working hours: %i" % (cumulative_hours[-1]))

    # Analyze data
    plotDataPerDay(total_days, hours, "Hours per day", "Hours")
    plotDataPerDay(total_days, cumulative_hours, "Cumulative hours", "Hours")

    # Analyze progress
    if name_of_progress is not None:
        absolute_progresses = getAbsoluteProgresses(cumulative_progresses)
        progresses_per_hours = getAbsoluteProgressPerHours(
            absolute_progresses, hours)
        average_efficiency = cumulative_progresses[-1] / cumulative_hours[-1]
        print("Average efficiency:", average_efficiency)
        plotDataPerDay(
            total_days, progresses_per_hours,
            name_of_progress.title() + " per hours",
            name_of_progress.title() + " / hour", values_can_be_negative=True)
        plot2Datasets(
            total_days, hours, absolute_progresses,
            "Working hours and absolute " + name_of_progress, "Hours",
            name_of_progress.title(), "working hours",
            "absolute " + name_of_progress, values_can_be_negative=True)
        plot2Datasets(
            total_days, hours, cumulative_progresses,
            "Working hours and cumulative " + name_of_progress, "Hours",
            name_of_progress.title(), "working hours",
            "cumulative " + name_of_progress)
        plot2Datasets(
            total_days, cumulative_hours, cumulative_progresses,
            "Cumulative working hours and cumulative " + name_of_progress,
            "Hours", name_of_progress.title(), "working hours",
            "cumulative " + name_of_progress)
    
if __name__ == "__main__":
    main()
