"""This module make a new directory and database files that are required for saving reports.

"reports_data/" directory that includes:
    - daily_reports.sqlite
    - daily_reports.xlsx
    - daily_reports.json
"""


import os
import sqlite3
import json
from typing import Protocol
from datetime import datetime, timedelta

import openpyxl

import input_validation


class FirstRun():
    """All configurations for program first run"""

    def __init__(self):
        if create_directory():
            print('This is your first run')
            first_day = get_first_day()
            CreateSQLiteDatabase().create(first_day)
            CreateExcelDatabase().create(first_day)
            CreateJsonDatabase().create(first_day)
        else:
            print('This is not your first run!')


def create_directory():
    try:
        os.mkdir('reports_data/')
        print('Created "reports_data/" directory')
        return True
    except FileExistsError:
        return False


def get_first_day():
    """Get project's first day"""
    today = datetime.today().date().isoformat()
    # check if user wants to start from today?
    print(f'Do you want to start from today {today}?')
    while True:
        user_choice = input('Press Yes/No:  ').strip().lower()
        if user_choice in ['y', 'n', 'yes', 'no']:
            break
    # set first_day based on user input
    if user_choice in ['yes', 'y']:
        first_day = today
        print('Today will be your first day ;)')
    else:
        first_day = input(
            'Enter a valid date according to YYYY/MM/DD fromat: ')
        first_day = input_validation.DateValidation().validate(first_day)
    return first_day


class CreateDatabase(Protocol):
    """Creating new database based on first day"""

    def create(self, first_day):
        pass


class CreateSQLiteDatabase():
    """Creating a sqlite3 database for five years report (~2200 days report)"""

    def create(self, first_day):
        if not os.path.exists('reports_data/daily_reports.sqlite'):
            # connect to database obj (create new one if db doesn't exists)
            print('Creating a new sqlite3 database ... (take a few seconds)')
            conn = sqlite3.connect(
                'reports_data/daily_reports.sqlite', isolation_level=None)
            # create "report" table with three columns "date", "study_work_hours", "explanation"
            conn.execute(
                'create table if not exists report (date text primary key, study_work_hours real, explanation text)')
            # add five years from first day
            for i in range(2200):
                day = first_day + timedelta(days=i)
                day = day.isoformat()   # convert to standard string format
                conn.execute('insert into report values (?, ?, ?)',
                             [day, None, None])
            conn.commit()
            conn.close()
            print('New SQLite3 database is made in "reports_data" directory')


class CreateExcelDatabase():
    """Creating a excel database for five years report (~2200 days report)"""

    def create(self, first_day):
        if not os.path.exists('reports_data/daily_reports.xlsx'):
            print('Creating a new excel database ... (take a few seconds)')
            # create a new workbook
            excel_file = openpyxl.Workbook()
            # rename defualt sheet
            excel_file['Sheet'].title = 'TenTousandHoursReport'
            # default values of some cells in each sheet
            cells = {
                'A1': 'date',
                'B1': 'study_work_hours',
                'C1': 'explanation',
            }
            for cell, value in cells.items():
                excel_file['TenTousandHoursReport'][cell] = value

            for i in range(2200):
                day = first_day + timedelta(days=i)
                day = day.isoformat()   # convert to standard string format
                excel_file['TenTousandHoursReport'][f'A{i+2}'] = day

            excel_file.save('reports_data/daily_reports.xlsx')
            print('New excel database is made in "reports_data" directory')


class CreateJsonDatabase():
    """Creating a json database for five years report (~2200 days report)"""

    def create(self, first_day):
        if not os.path.exists('reports_data/daily_reports.json'):
            print('Creating a new json database ... (take a few seconds)')
            days = {}
            for i in range(2200):
                day = datetime.today().date() + timedelta(days=i)
                day = day.isoformat()
                days.setdefault(day)

            with open('reports_data/daily_reports.json', mode='w') as file:
                json.dump(days, file, indent=4)

            print('New json database is made in "reports_data" directory')


if __name__ == '__main__':
    try:
        FirstRun()
    except KeyboardInterrupt:
        os._exit(0)
