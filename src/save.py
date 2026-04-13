"""This module can save daily reports to databases"""
import sqlite3
import json
from typing import Protocol
from datetime import datetime, timedelta


class SaveReport(Protocol):
    """Save report to database"""

    def save(self, date, study_hours, explanation):
        pass


class SQLiteDatabaseSaveReport():
    def save(self, date, study_hours, explanation):
        self.date = date.isoformat()
        conn = sqlite3.connect(
            'reports_data/daily_reports.sqlite', isolation_level=None)
        conn.execute('update report set study_work_hours = (?) where date = (?)', [
                     study_hours, self.date])
        conn.execute('update report set explanation = (?) where date = (?)', [
                     explanation, self.date])
        conn.commit()
        conn.close()
        print(f'Report of {self.date} is done')


class JsonSaveReport():
    def save(self, date, study_hours, explanation):
        self.date = date.isofromat()
        with open('reports_data/last_report.json', mode='r') as file:
            json_file = json.load(file)

          json_file[f'{self.date}']


class ExcelSaveReport():
    def save(self):
        pass
