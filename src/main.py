"""This program developed by me"""

import os
import json
from datetime import datetime, timedelta
import sqlite3
from typing import Protocol

import input_validation
import achievement
import save
import first_run


if os.getcwd().split('/')[-1] == 'project_10_000_hours_python':
    REPORTS_DIR = 'reports_data'
elif os.getcwd().split('/')[-1] == 'src':
    REPORTS_DIR = '../reports_data'
else:
    print('Maybe you change projects directory name.\n go to src/ and run again.')
    os._exit()


def main():
    # decide to run first run or not
    if not os.path.exists(f'{REPORTS_DIR}/daily_reports.sqlite'):
        first_run.FirstRun()
    first_day_date, days_without_reports = days_need_report()
    decide_about_get_report(first_day_date, days_without_reports)
    decide_about_achievement()


def days_need_report():
    # open json file
    with open(f'{REPORTS_DIR}/daily_reports.json') as file:
        daily_reports = json.load(file)
    # get first day without report
    for date in daily_reports:
        if daily_reports[date] == None:
            first_day_date = date
            break
    # convert first day to date object
    first_day_date = datetime.strptime(
        first_day_date, "%Y-%m-%d").date() - timedelta(1)
    today = datetime.today().date()
    # get number of days that don't have report
    days_without_reports = (today - first_day_date).days
    print(
        f'From {first_day_date} to {today}, there is {days_without_reports} days without report')
    return first_day_date, days_without_reports


def decide_about_get_report(first_day_date, days_without_reports):
    today = datetime.today().date()
    # ask user if want to add reports
    msg = f'Do you want to add report? (Press y/n): '
    if days_without_reports == 0:
        pass
    elif input_validation.YesNoValidation().validate(msg):
        for i in range(days_without_reports):
            date = first_day_date + timedelta(i)
            if date == today:
                msg = 'Today\'s report is ready? (Press y/n): '
                if input_validation.YesNoValidation().validate(msg):
                    study_hours, explanation = get_report(date)
                    save.JsonSaveReport().save(date, study_hours, explanation)
                    # save.ExcelSaveReport().save(date, study_hours, explanation)
                    # save.SQLiteDatabaseSaveReport().save(date, study_hours, explanation)
                    print(f'Report of {date} is done')
            else:
                study_hours, explanation = get_report(date)
                save.JsonSaveReport().save(date, study_hours, explanation)
                # save.ExcelSaveReport().save(date, study_hours, explanation)
                # save.SQLiteDatabaseSaveReport().save(date, study_hours, explanation)
                print(f'Report of {date} is done')


def decide_about_achievement():
    # ask user if want to view achievement
    msg = 'Do you want to see you achievements report? (Press y/n): '
    if input_validation.YesNoValidation().validate(msg):
        achievement.main()


def get_report(date):
    print('*' * 16)
    print(f'Date: {date}')
    print('*' * 16)
    msg = 'How many hours did you study/work? (should be multiple of 0.5 hours): '
    study_hours = input_validation.HoursValidation().validate(msg)
    msg = 'Explain in less than 80 character what did you do?'
    explanation = input_validation.ExplanationValidation().validate(msg)
    return study_hours, explanation


if __name__ == '__main__':
    try:
        os.system('cls' if os.__name__ == 'nt' else 'clear')
        main()
    except KeyboardInterrupt:
        os._exit(1)
