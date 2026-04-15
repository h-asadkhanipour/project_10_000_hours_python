"""This module can save daily reports to databases"""
import sqlite3
import json
import os
from typing import Protocol
from datetime import datetime

import openpyxl


if os.getcwd().split('/')[-1] == 'project_10_000_hours_python':
    REPORTS_DIR = 'reports_data'
elif os.getcwd().split('/')[-1] == 'src':
    REPORTS_DIR = '../reports_data'
else:
    print('Maybe you change projects directory name.\n go to src/ and run again.')
    os._exit()


class SaveReport(Protocol):
    """Save report to database"""

    def save(self, date, study_hours, explanation):
        pass


class SQLiteDatabaseSaveReport():
    def save(self, date, study_hours, explanation):
        self.date = date
        # connect to sqlite database
        conn = sqlite3.connect(
            f'{REPORTS_DIR}/daily_reports.sqlite', isolation_level=None)
        # update study hours column based on date
        conn.execute('update report set study_work_hours = (?) where date = (?)', [
                     study_hours, self.date])
        # update explanation column based on date
        conn.execute('update report set explanation = (?) where date = (?)', [
                     explanation, self.date])
        # save and close connection to database
        conn.commit()
        conn.close()
        # print success
        print(f'Report of {self.date} saved to daily_reports.sqlite')


class JsonSaveReport():
    def save(self, date, study_hours, explanation):
        self.date = date
        # open json file
        with open(f'{REPORTS_DIR}/daily_reports.json', mode='r') as file:
            json_file = json.load(file)
        # edit json file base on date as key
        json_file[f'{self.date}'] = {
            'study_work_hours': study_hours,
            'explanation': explanation,
        }
        # save json file
        with open(f'{REPORTS_DIR}/daily_reports.json', mode='w') as file:
            json.dump(json_file, file, indent=4)
        # print success
        print(f'Report of {self.date} saved to daily_reports.json')


class ExcelSaveReport():
    def save(self, date, study_hours, explanation):
        self.date = date
        # open excel file
        excel_file = openpyxl.load_workbook(
            f'{REPORTS_DIR}/daily_reports.xlsx')
        excel_sheet = excel_file['TenThousandHoursReport']
        # find index based on fisrt day in A2
        first_day = excel_sheet['A2'].value
        first_day = datetime.strptime(first_day, "%Y-%m-%d").date()
        column_date_index = (date - first_day).days
        # save report
        excel_sheet[f'B{column_date_index}'] = study_hours
        excel_sheet[f'C{column_date_index}'] = explanation
        # close excel
        excel_file.close()
        # print success
        print(f'Report of {self.date} saved to daily_reports.xlsx')
