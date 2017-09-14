# -*- coding: utf-8 -*-
# !C:/Program Files (x86)/Python 3.5/python.exe

import os
import datetime  # Umwandlung von Datum in Wochentag
import glob   # zum öffnen mehrerer files
import csv  # comma separated value
import sqlite3  # sqlite3 database support
import pandas as pd
import matplotlib.pyplot as plt
# import seaborn as sns

# HIER WAR DER PENIS MANN


def open_files():
    """
    This function opens all *.log files in the 'log' directory.
    every line is a file, which is opened, read line by line and the content
    of the variable "lines" can be accessed globally. the data converter
    function takes this content and writes the interesting parts into
    gcdata.txt
    """
    files = glob.glob("logs/*.log")
    print("Files found in log file directory:\n")
    print("____________________________________________\n", files)
    global lines
    lines = []
    file_counter = 0
    try:
        with open("logs/log_history", "r+") as log_history:
            print(log_history)
            log_list = [line.rstrip() for line in log_history]
            for file in files:
                if file not in log_list:
                    f_open = open(file, 'r')
                    lines.extend(f_open.readlines())
                    f_open.close()
                    log_history.write(file + "\n")
                    file_counter += 1
                else:
                    pass
        print("\nexisting log_history used!\n")
    except:
        with open("logs/log_history", 'w') as log_history:
            for file in files:
                log_history.write(file + "\n")
                f_open = open(file, 'r')
                lines.extend(f_open.readlines())
                f_open.close()
                file_counter += 1
            print("new log history created!\n")
    print(file_counter, "new files loaded!\n")


def data_converter():
    """
    Funktion die die Dateinamen der gemessenen Chromatogramme in
    Außerdem werden die Daten in Wochentage umgewandelt.
    Dazu werden die eingelesenen logfiles Zeile für Zeile durchsucht.
    Zu Beginn der Funktion wird ein csv-file geöffnet und der output
    hineingeschrieben
    """
    ofile = open('gcdata.txt', "w")
    writer = csv.writer(ofile, delimiter='\t', )
    log_list = open("logs/log_history", 'r')  # liste der logs öffnen
    for log in log_list:  # für jede Datei in log_list:
        with open(log.rstrip(), "r") as lines:
            # öffne die logdatei ohne Zeilenumbruch
            for line in lines:  # und für jede Zeile:
                line_stuff = line.split()
                if line_stuff[0] == "RMETHOD" and line_stuff[1] == 'Acquired':
                    try:
                        weekday = datetime.datetime.strptime(
                                    line_stuff[4], '%m/%d/%Y').strftime('%A')
                        print(line_stuff[3], line_stuff[4], weekday)
                        output = [line_stuff[3], line_stuff[4], weekday]
                        writer.writerow(output)
                    except (IndexError, ValueError):
                        # manchmal sind Leerzeichen im run-title, dann muss
                        # der list-index anders sein
                        weekday = datetime.datetime.strptime(
                                    line_stuff[5], '%m/%d/%Y').strftime('%A')
                        print(line_stuff[4], line_stuff[5], weekday)
                        output = [line_stuff[4], line_stuff[5], weekday]
                        writer.writerow(output)
                    else:
                        pass
    ofile.close()
    log_list.close()


def SQL_converter(x):  # create oder input
    """
    Diese Funktion soll das output file 'gcdata.txt' in eine SQLite Datenbank
    einfügen. Zuerst wird eine Standardverbindung
    über die Python API zur Datenbank aufgebaut. Wenn der Param. 'create' ist,
    wird eine Tabelle in der Datenbank angelegt. Ist der Param. 'input', so
    sollen die Daten aus gcdata.txt in die Tabelle eingefügt werden.
    """
    connection = sqlite3.connect("gc.db")
    cursor = connection.cursor()
    if x == 'create':
        ofile = open('gcdata.txt', "r")
        sql_command = """
        CREATE TABLE gcdata (
        run INTEGER PRIMARY KEY,
        time time,
        date date,
        weekday VARCHAR(80),
        CONSTRAINT unq UNIQUE (time, date));
        """
        cursor.execute(sql_command)  # Befehl ausführen
        connection.commit()  # Befehl abschicken
        connection.close()  # Verbindung schließen

    elif x == 'input':
        print('''Entries are added to the database. \n
                This can take several minutes. Please wait.''')
        ofile = open('gcdata.txt', "r")
        ofile2 = csv.reader(ofile, delimiter='\t',)
        connection = sqlite3.connect("gc.db")
        cursor = connection.cursor()
        for row in ofile2:
            try:
                format_str = """
                INSERT OR IGNORE INTO gcdata (
                time,
                date,
                weekday)
                VALUES(
                '{0}',
                '{1}',
                '{2}')
                """.format(row[0], row[1], row[2])
                # Eingabe der Variablen funktioniert nur, wenn
                # List Index Error umgangen wird.
                cursor.execute(format_str)
            except IndexError:
                pass
        connection.commit()
        print("Operation successful!")
        connection.close()
    else:
        pass


def check_entries():
    # abrufen der Daten und ausgabe selbiger in der Konsole, um zu sehen,
    # ob alles funktioniert hat
    entries = 0
    connection = sqlite3.connect("gc.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM gcdata")
    result = cursor.fetchall()
    for r in result:
        entries += 1
        print(r)
    connection.close()
    print(entries, "entries in the database.")


# STATISTICS
weekdays = ['Monday', 'Tuesday', 'Wednesday',
            'Thursday', 'Friday', 'Saturday', 'Sunday']


def describe():
    con = sqlite3.connect(r'gc.db')
    df = pd.read_sql_query("SELECT * FROM gcdata", con)
    df['date'] = pd.to_datetime(df.date)
    start = input('Start:')
    end = input('End:')
    injections_per_day = df['date'].value_counts()
    injections_per_day = injections_per_day.loc[str(start):str(end)]
    print(injections_per_day.describe())


def total_injections_plot():
    # total number of injections per date + description of data
    con = sqlite3.connect(r'gc.db')
    df = pd.read_sql_query("SELECT * FROM gcdata", con)
    df['date'] = pd.to_datetime(df.date)
    start = input('Start:')
    end = input('End:')
    injections_per_day = df['date'].value_counts()
    injections_per_day = injections_per_day.sort_index()
    injections_per_day = injections_per_day.loc[str(start):str(end)]
    injection_plot = injections_per_day.plot()
    # plot(kind='bar') sieht gut aus, funktioniert aber nicht als overlay
    injections_per_day.rolling(window=30).mean().plot(ax=injection_plot)
    # .expanding().mean() zeichnet kumulierten Durchschnitt
    # ax=injection_plot zeichnet injections_per_day.plot() in
    # den expanding-means-plot
    plt.title('Total number of injections per date')
    injection_plot.axes.get_xaxis().set_ticks([])
    print(str(injections_per_day.describe()))
    plt.show()


# NOT WORKING RIGHT?!
def total_injections_hist():
    #  total number of times a certain number of injections ocurred on one day
    con = sqlite3.connect(r'gc.db')
    df = pd.read_sql_query("SELECT * FROM gcdata", con)
    df['date'] = pd.to_datetime(df.date)
    start = input('Start:')
    end = input('End:')
    injections_per_day = df['date'].value_counts()
    injections_per_day = injections_per_day.sort_index()
    injections_per_day = injections_per_day.loc[str(start):str(end)]
    plt.hist(injections_per_day, 25, normed=1, facecolor='g', alpha=0.75)
    plt.title('''Number of times a certain number of \n
                injections ocurred on a single day''')
    plt.show()


# grouping not working!
def injections_per_weekday():
    # total number of injections grouped by day of the week
    con = sqlite3.connect(r'gc.db')
    df = pd.read_sql_query("SELECT * FROM gcdata", con)
    df['date'] = pd.to_datetime(df.date)
    start = input('Start:')
    end = input('End:')
    df = df.set_index(['date'])
    # date muss index sein, damit loc die einträge findet
    injections_per_day = df.loc[str(start):str(end)]
    injections_per_weekday = injections_per_day['weekday'].value_counts()
    injections_per_weekday = injections_per_weekday.reindex(weekdays)
    # sorts weekdays naturally
    print(injections_per_weekday)
    injections_per_weekday.plot(kind='bar')
    plt.title('Total number of injections from\n' + start + ' to ' + end +
              '\ngrouped by day of the week')
    plt.show()

# main


menu = """
Welcome to GCStat!
Type the number of the action you want to perform.
1. Load logbooks
2. Extract data
3. Create and fill database
4. Print database to screen
5. Enter statistics mode
Type 'reset' to delete database and log_history.
Type 'exit' to exit.
Type 'help' for help.
"""

statsmenu = """

=== STATISTICS ===
Type the number of the action you want to perform.
Most stats use a time frame. Use the format 'yyyy-mm-dd'.

1. Show general stats for a given time frame
2. Show total number of injections per day (date) in a given time frame
3. Show total number of injections per weekday in a given time frame
4.
5. Return to previous mode
"""


helpx = """
=== HELP ===

1:
Loads all logbook files in the 'logs' folder and checks whether they
are new or have been analysed before. 'log_history' is created, which contains
a list of all log files that will be used for data extraction.

2:
Cuts all dates and times from the collected logbook data and
computes the corresponding weekdays. The output is intermittendly saved to
'gcdata.txt' and can be opened with Excel import wizard.

3:
Creates an SQLite3 database 'gc.db'. All data from gcdata.txt is then added to
this database and can be accessed with an SQLite Client. Free Software for
Windows is 'SQLiteBrowser' and for Unix Systems you can use the SQLite3 Shell.
At the moment it is possible to create duplicate entries in the database,
by repeatedly using option 3. You should therefore reset the database every
time before you fill the database when the logs folder contains already used
log files.

4:
Prints the whole database to the screen. yay.

5:
Enters statistics mode and shows available actions for statistical analysis.

reset:
Deletes all data that might cause duplicate or wrong entries in the gcdata.txt
or database.

Note:
A typical workflow for running the script for the first time would be to
do 1,2,3 and then go into statistics mode
"""

while True:
    print(menu)
    choice = input('Choice:')
    if choice == "1":
        open_files()
    elif choice == "2":
        try:
            data_converter()  # Daten aus Quelle in gcdata.txt exportieren
        except:
            raise
    elif choice == "3":
        try:  # es wird versucht eine Tabelle anzulegen, falls keine existiert
            SQL_converter('create')
            print("new database created!")
        except:
            pass
        SQL_converter('input')  # Daten werden in die Datenbank eingepflegt
    elif choice == "4":
        check_entries()
    elif choice == "exit":
        break
    elif choice == "reset":
        os.remove("logs/log_history")
        os.remove("gc.db")
        os.remove("gcdata.txt")
    elif choice == "help":
        print(helpx)
    if choice == "5":
        while True:
            print(statsmenu)
            choice2 = input('Choice:')
            if choice2 == "1":
                describe()
            elif choice2 == "2":
                total_injections_plot()
            elif choice2 == "3":
                injections_per_weekday()
            # elif choice == "4":
            elif choice2 == "5":
                break
