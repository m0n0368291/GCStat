# GCStat
GCStat is an interactive script to read out logbook files of GC/MS Systems and do statistical analysis of activity und overall performance.

## Features

- Parses logbook files and inserts information into an SQLite3 database
- Performs statistical calculations
- Generates various reports

Example reports are given below:

![Total number of injections in given time frame sorted by weekday](https://github.com/m0n0368291/GCStat/blob/master/tot_inj_date.bmp)

![Total number of injections in given time frame sorted by weekday](https://github.com/m0n0368291/GCStat/blob/master/tot_inj_weekday.bmp)

![Total number of injections in given time frame shown as count plot](https://github.com/m0n0368291/GCStat/blob/master/tot_inj_countplot.bmp)

## Getting Started
- Install Python 3.X and Git from official sources like [Python.org](https://www.python.org/) or [git-scm.com](https://git-scm.com/download/win)
- Clone into this repository with ``git clone https://github.com/m0n0368291/GCStat.git``
- Create a folder named ``log`` in the same directory as ``main.py`` which contains all GCMS logfiles
- Execute ``main.py`` by typing ``python main.py`` into the command-line, after navigating into the folder containing the repository
- The command-lin interface will give you further instructions. For help just type ``help``.

## List of (planned) functions

- [x] read logbook files into SQLite3 database
- [x] respect privacy and not read user data
- [x] give a short report of analyses for a given time frame
- [x] output a plot for all sample analyses in a given time frame
- [x] output a plot for all sample analyses in i given time frame grouped by day of week
- [x] histogram for injections per day

## Notes & Help

If you need any help, contact me via [email](christopher_grimm@gmx.de)
