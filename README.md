# Work Hours Timeline

## 1 Introduction

This script visualizes working hours on timeline. It also calculates the cumulative working hours and shows it as well. Here are some images to show the output.

![Hours per day graph](images/hours_per_day_1.png)

The first graph shows hours done in each marked day.

![Cumulative hours graph](images/cumulative_hours_1.png)

The second graph shows cumulative hours in each marked day.

![Denser timeline](images/denser_timeline.png)

The third graph is the same as first one but shows denser timeline which can be defined by changing the constant variables defined in the beginning of the code.

## 2 Installation

1. Install Python. Python 3.6 has been used during development but this should work with all Python 3 versions.

1. Install libraries: `pip install -r requirements.txt`

## 3 Running the Code

The code needs to know the file name and delimiter used in CSV file. These could be changed directly inside the code or another option is to give them as command line arguments. Run the code from bash in a following way:

```bash
python main.py <file_name> <delimiter>
```

Examples:

```bash
python main.py work_hours.csv ,
python main.py work_hours.csv
python main.py
```
