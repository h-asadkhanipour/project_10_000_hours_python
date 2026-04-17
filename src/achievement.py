import sqlite3
import json
import os
from datetime import datetime, timedelta
from typing import Protocol

from sev_seg_display import SevSeg
import input_validation


DAYS_TO_IGNORE = ['holiday', 'sick day',]

if os.getcwd().split('/')[-1] == 'project_10_000_hours_python':
    REPORTS_DIR = 'reports_data'
elif os.getcwd().split('/')[-1] == 'src':
    REPORTS_DIR = '../reports_data'
else:
    print('Maybe you change projects directory name.\n go to src/ and run again.')
    os._exit()


def main():
    # check whether daily_report are update or not
    if check_update():
        today = datetime.today().date()
        yesterday = datetime.today().date() - timedelta(1)
        if os.path.exists(f'{REPORTS_DIR}/last_report.json'):
            json_file = JsonUpdateProgress()
            if json_file.last_report_date in [today, yesterday]:
                achievement_hours = json_file.achievement_hours
                total_days = json_file.total_days
        else:
            sqlite_file = SqliteUpdateProgress()
            achievement_hours = sqlite_file.achievement_hours
            total_days = sqlite_file.total_days
        # calculate last progress
        progress = Progress()
        progress.calculate(achievement_hours, total_days)
        # save last progress to json
        progress.save_to_json()
        # show last progress
        progress.show_progress()
    else:
        print('Reports are not update')
        msg = 'Do you want to update achievement reports? (Press y/n): '
        if input_validation.YesNoValidation().validate(msg):
            sqlite_file = SqliteUpdateProgress()
            achievement_hours = sqlite_file.achievement_hours
            total_days = sqlite_file.total_days
            # calculate last progress
            progress = Progress()
            progress.calculate(achievement_hours, total_days)
            # save last progress to json
            progress.save_to_json()
            # show last progress
            progress.show_progress()
        else:
            progress = Progress()
            progress.get_from_last_report()
            progress.show_progress()


def check_update():
    # load daily_report.json file
    with open(f'{REPORTS_DIR}/daily_reports.json') as file:
        daily_reports = json.load(file)
    # get today as a string
    today = datetime.today().date().isoformat()
    # check today has a report or not
    if daily_reports[f'{today}'] != None:
        return True
    return False


class UpdateProgress(Protocol):
    def __init__(self):
        pass

    def calculate_achievement_hours_total_days(self):
        pass


class JsonUpdateProgress():
    """This class is used when last report was yesterday"""

    def __init__(self):
        # open json file
        with open(f'{REPORTS_DIR}/last_report.json', mode='r') as file:
            self.last_report = json.load(file)
        # get last report date
        last_report_date = self.last_report['last_report_date']
        # convert string to date object
        self.last_report_date = datetime.strptime(
            last_report_date, "%Y-%m-%d").date()
        # get achievement hours and total days
        self.achievement_hours = self.last_report['achievement_hours']
        self.total_days = self.last_report['total_days']
        # update achievement hours and total days
        if self.last_report_date == (datetime.today().date() - timedelta(1)):
            self.calculate_achievement_hours_total_days()

    def calculate_achievement_hours_total_days(self):
        # convert today's date object to string
        today = datetime.today().date().isoformat()
        # open daily_reports.json
        with open(f'{REPORTS_DIR}/daily_reports.json', mode='r') as file:
            json_file = json.load(file)
        # get study hours of today
        today_study_hours = json_file[f'{today}']['study_work_hours']
        today_explanation = json_file[f'{today}']['explanation']
        # ignore holidays
        if today_explanation not in DAYS_TO_IGNORE:
            self.achievement_hours += today_study_hours
            self.total_days += 1


class SqliteUpdateProgress():
    def __init__(self):
        # connect to database
        conn = sqlite3.connect(
            f'{REPORTS_DIR}/daily_reports.sqlite', isolation_level=None)
        self.results = conn.execute(
            'select * from report where study_work_hours != "None"').fetchall()
        # calculate achievement hours and total days
        self.calculate_achievement_hours_total_days()

    def calculate_achievement_hours_total_days(self):
        total_days = 0
        achievement_hours = 0
        for result in self.results:
            if result[2] not in DAYS_TO_IGNORE:
                total_days += 1
                achievement_hours += result[1]
        self.achievement_hours = achievement_hours
        self.total_days = total_days


class Progress():
    def calculate(self, achievement_hours, total_days):
        # calculate progress
        self.achievement_hours = achievement_hours
        self.total_days = total_days
        self.achievement_percent = (achievement_hours / 10_000) * 100
        self.mean_hours_per_day = (achievement_hours / self.total_days)
        self.hours_to_end = 10_000 - achievement_hours
        self.days_to_end = self.hours_to_end / self.mean_hours_per_day
        self.weeks_to_end = self.days_to_end / 7
        self.months_to_end = self.days_to_end / 30
        self.years_to_end = self.days_to_end / 365
        celebration_day = datetime.today().date() + timedelta(days=self.days_to_end)
        self.celebration_day = celebration_day.isoformat()

    def save_to_json(self):
        # get first day from daily_reports.json
        with open(f'{REPORTS_DIR}/daily_reports.json') as file:
            daily_reports = json.load(file)
        self.first_day = next(iter(daily_reports))
        # find last reports date from daily_reports.json
        for date in daily_reports:
            if daily_reports[date] == None:
                last_report_date = (datetime.strptime(
                    date, '%Y-%m-%d').date() - timedelta(1)).isoformat()
                break
        # save it to json
        self.last_report_date = last_report_date
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
            'celebration_day': self.celebration_day,
        }
        with open(f'{REPORTS_DIR}/last_report.json', mode='w') as file:
            json.dump(last_report, file, indent=4)

    def get_from_last_report(self):
        # load json file
        with open(f'{REPORTS_DIR}/last_report.json') as file:
            last_report = json.load(file)
        # get items of last report
        self.last_report_date = last_report['last_report_date']
        self.first_day = last_report['first_day']
        self.total_days = last_report['total_days']
        self.achievement_hours = last_report['achievement_hours']
        self.achievement_percent = last_report['achievement_percent']
        self.mean_hours_per_day = last_report['mean_hours_per_day']
        self.hours_to_end = last_report['hours_to_end']
        self.days_to_end = last_report['days_to_end']
        self.weeks_to_end = last_report['weeks_to_end']
        self.months_to_end = last_report['months_to_end']
        self.years_to_end = last_report['years_to_end']
        self.celebration_day = last_report['celebration_day']

    def show_progress(self):
        print()
        print('*' * 80)
        print('*** Achievement report:')
        print('*' * 80)
        print()
        print('Your pregress is:\t',
              f'{self.achievement_percent:.2f}\tpercent')
        print('You have achieved:\t', f'{self.achievement_hours}\thours')
        print()
        print('You have started this project in:\t', self.first_day)
        print('You have Studied/Worked for:\t\t', self.total_days, 'days')
        print('Your mean Study/Work hours is:\t\t',
              f'{self.mean_hours_per_day:.1f}')
        print()
        print('Estimated days to achieve your goal:\t\t\t\t',
              f'{self.days_to_end:.0f}', 'days')
        print('Estimated weeks to achieve your goal:\t\t\t\t',
              f'{self.weeks_to_end:.0f}', 'weeks')
        print('Estimated months to achieve your goal:\t\t\t\t',
              f'{self.months_to_end:.0f}', 'months')
        print('Estimated years to achieve your goal:\t\t\t\t',
              f'{self.years_to_end:.0f}', 'years')
        print('Based on your average study hours, celebration day would be:')
        print()
        num1, num2, num3 = self.celebration_day.split(sep='-')
        SevSeg(num1, num2, num3, separator='/')
        print()


if __name__ == '__main__':
    try:
        os.system('cls' if os.__name__ == 'nt' else 'clear')
        main()
    except KeyboardInterrupt:
        os._exit(0)
