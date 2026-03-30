import sqlite3
import json
import os
from datetime import datetime, timedelta

from sev_seg_display import SevSeg


class Achievement():
    def __init__(self):
        self.conn = sqlite3.connect('sqlite3_db/database.db', isolation_level=None)
        self.today = datetime.today().date()
        self.yesterday = self.today - timedelta(days=1)
        self.update_progress()
        self.show_progress()

    def update_progress(self):
        # decide to use last json report or recalculate
        if os.path.exists('reports/last_report.json'):
            self.get_last_report_date()
            if self.last_report_date in [self.yesterday, self.today]:
                self.use_last_json_progress()
            else:
                self.calculate_database_progress()
        else:
            self.calculate_database_progress()

    def get_last_report_date(self):
        with open('reports/last_report.json', mode='r') as file:
            last_report = json.load(file)
        last_report_date = last_report['last_report_date']
        self.last_report_date = datetime.strptime(last_report_date, "%Y-%m-%d").date()
    
    def calculate_database_progress(self):
        # connect to database
        results = self.conn.execute('select * from report where study_work_hours != "None"').fetchall()
        # calculate total number of days (except holidays) and achievement hours
        self.first_day = results[0][0]
        total_days = 0
        achievement_hours = 0
        for result in results:
            if result[2] != 'holiday':
                total_days += 1
                achievement_hours  += result[1] 
        self.total_days = total_days
        self.achievement_hours = achievement_hours
        self.achievement_percent = (achievement_hours /10_000) * 100
        self.mean_hours_per_day = (achievement_hours / self.total_days)
        self.hours_to_end = 10_000 - achievement_hours
        self.days_to_end = self.hours_to_end / self.mean_hours_per_day
        self.weeks_to_end = self.days_to_end / 7
        self.months_to_end = self.days_to_end / 30
        self.years_to_end = self.days_to_end / 365
        self.celebration_day = datetime.today().date() + timedelta(days=self.days_to_end)
        # save it to json
        self.last_report_date = datetime.today().date().isoformat()
        last_report = {
        'last_report_date': self.last_report_date,
        'first_day': self.first_day,
        'total_days': self.total_days, 
        'achievement_hours': self.achievement_hours, 
        'achievement_percent': self.achievement_percent, 
        'mean_hours_per_day': self.mean_hours_per_day, 
        'hours_to_end': self.hours_to_end, 
        'days_to_end': self.days_to_end, 
        'weeks_to_end': self.weeks_to_end, 
        'months_to_end': self.months_to_end, 
        'years_to_end': self.years_to_end, 
        'celebration_day': self.celebration_day.isoformat(), 
        }
        with open('reports/last_report.json', mode='w') as file:
            json.dump(last_report, file, indent=4)

    def use_last_json_progress(self):
        # load json file
        with open('reports/last_report.json', mode='r') as file:
            last_report = json.load(file)
        # check if last report is for today or for yesterday
        if self.last_report_date == self.yesterday:
            # get today report from database
            date = datetime.today().date().isoformat()
            today_report_hours = self.conn.execute('select * from report where date = (?)', [date]).fetchall()[0][1]
            # use last report to set achievement hours and total days
            achievement_hours = last_report['achievement_hours'] + today_report_hours
            self.total_days = last_report['total_days'] + 1 
        else:
            achievement_hours = last_report['achievement_hours']
            self.total_days = last_report['total_days']
        # get first day from json
        self.first_day = last_report['first_day']
        # calculate progress 
        self.achievement_hours = achievement_hours
        self.achievement_percent = (achievement_hours /10_000) * 100
        self.mean_hours_per_day = (achievement_hours / self.total_days)
        self.hours_to_end = 10_000 - achievement_hours
        self.days_to_end = self.hours_to_end / self.mean_hours_per_day
        self.weeks_to_end = self.days_to_end / 7
        self.months_to_end = self.days_to_end / 30
        self.years_to_end = self.days_to_end / 365
        self.celebration_day = datetime.today().date() + timedelta(days=self.days_to_end)

    def show_progress(self):
        print()
        print('*' * 79)
        print('*** Achievement report:')
        print('*' * 79)
        print()
        print('Your pregress is:\t', f'{self.achievement_percent:.2f}\tpercent')
        print('You have achieved:\t', f'{self.achievement_hours}\thours')
        print()
        print('You have started this project in:\t', self.first_day)
        print('You have Studied/Worked for:\t\t', self.total_days, 'days')
        print('Your mean Study/Work hours is:\t\t', f'{self.mean_hours_per_day:.1f}')
        print()
        print('Estimated days to achieve your goal:\t\t\t\t', f'{self.days_to_end:.0f}', 'days')
        print('Estimated weeks to achieve your goal:\t\t\t\t', f'{self.weeks_to_end:.0f}', 'weeks')
        print('Estimated months to achieve your goal:\t\t\t\t', f'{self.months_to_end:.0f}', 'months')
        print('Estimated years to achieve your goal:\t\t\t\t', f'{self.years_to_end:.0f}', 'years')
        print('Based on your average study hours, celebration day would be:')
        print()
        num1, num2, num3 = self.celebration_day.isoformat().split(sep='-')
        SevSeg(num1, num2, num3, separator='/')
        print() 


if __name__ == '__main__':
    Achievement()
