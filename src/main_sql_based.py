"""This program developed by me"""

import os
from datetime import datetime, timedelta
import sqlite3

from achievement import Achievement


class TenTousandHours():
    def __init__(self):
        self.clear_screen()
        self.today = datetime.today().date()
        if not self.check_database_available():
            self.first_run()
        self.yesterday = self.today - timedelta(days=1)
        self.first_day = None
        self.date = None
        self.last_report = None
        self.check_last_report()
        if self.last_report == self.today:
            print('>>> Your reports is update <<<')
            print(f'Today is: {self.today}')
        elif self.last_report == self.yesterday:
            self.get_report()
        else:
            self.get_multiple_reports()

    def first_run(self):
        """All configurations for program first run"""
        print('This is your first run')
        # ask user what is first day of journey
        self.get_first_day()
        # check whether sqlite3_db and reports directories exists
        try:
            os.mkdir('sqlite3_db/')
            os.mkdir('reports/')
        except FileExistsError:
            pass
        # create new database
        self.create_sqlite3_database()
        # get first report
        if self.first_day == self.today:
            self.get_report()
            os._exit(1)
        else:
            self.get_multiple_reports()
            os._exit(1)
    
    def get_first_day(self):
        """Only used for first run"""
        # check if user wants to start from today?
        print(f'Do you want to start from today {self.today}?')
        while True:
            user_choice = input('Press Yes/No:  ').strip().lower()
            if user_choice in ['y', 'n', 'yes', 'no']:
                break
            else:
                print(f'WARNING: user input {user_choice} is not valid !!!')
        # set first_day based on user input
        if user_choice in ['yes', 'y']:
            self.first_day = self.today
            self.last_report = self.today - timedelta(days= 1)
            print('Today will be your first day ;)')
        else:
            self.first_day  = self.get_valid_date()
            self.last_report = self.first_day - timedelta(days=1)

    def create_sqlite3_database(self):
        """Creating a sqlite3 database for five years report (~2200 days report)"""
        # connect to database obj (create new one if db doesn't exists)
        print('Creating a new sqlite3 database ... (take a few seconds)')
        conn = sqlite3.connect('sqlite3_db/database.db', isolation_level=None)
        # create "report" table with three columns "date", "study_work_hours", "explanation"
        conn.execute('create table if not exists report (date text primary key, study_work_hours real, explanation text)')
        # add five years from first day
        for i in range(2200):
            day = self.first_day + timedelta(days=i)
            day = day.isoformat()   # convert to standard string format
            conn.execute('insert into report values (?, ?, ?)', [day, None, None])
        conn.commit()
        print('New SQLite3 database is made in "sqlite3_db" directory')
        conn.close()

    def check_database_available(self):
        if os.path.exists('sqlite3_db/database.db'):
            return True
        else:
            return False

    def check_last_report(self):
        """Find last report"""
        # connect to database
        conn = sqlite3.connect('sqlite3_db/database.db', isolation_level=None)
        # get date string of last report
        last_report = conn.execute('select * from report where explanation != "None"').fetchall()[-1][0]
        # convert last report standard date srting to date format
        last_report = datetime.strptime(last_report, "%Y-%m-%d").date()
        self.last_report = last_report
        conn.close()

    def get_report(self):
        if self.date == None:
            self.date = self.today
        print(f'Date: {self.date}')
        study_hours = self.get_valid_hours()
        explanation = self.get_valid_explanation()
        # add report to database
        date = self.date.isoformat()
        conn = sqlite3.connect('sqlite3_db/database.db', isolation_level=None)
        conn.execute('update report set study_work_hours = (?) where date = (?)', [study_hours, date])
        conn.execute('update report set explanation = (?) where date = (?)', [explanation, date])
        conn.commit()
        conn.close()
        print(f'Report of {self.date} is done')
        print()
        print()

    def get_multiple_reports(self):
        # check if it is first run or not
        if self.first_day == None:
            days = (self.today - self.last_report).days 
        else:
            days = (self.today - self.first_day).days
        # take report according to number of days
        for day in range(days):
            self.date = self.last_report + timedelta(days= (day + 1))
            self.get_report()

    def get_valid_date(self):
        print('Enter a valid date according to YYYY/MM/DD format, for example 2026/01/01')
        while True:
            user_date = input('date = ').strip().lower()
            try:
                self.date = datetime.strptime(user_date, "%Y/%m/%d").date()
                break
            except ValueError:
                print(f'{user_date} is not a valid date')
        return self.date

    def get_valid_hours(self):
        print('How much hours did you work/study?')
        while True:
            study_hours = input('Enter a multiple of 0.5 hours (for example 6.5 hours): ')
            try:
                float(study_hours)
            except ValueError:
                print(f'{study_hours} is not valid')
                continue

            if 0<= float(study_hours) <= 18:
                if float(study_hours) % 0.5 == 0:
                    study_hours = float(study_hours)
                    break
                else:
                    print('Study/Work hour should be multiple of 0.5 (half hour)')
            else:
                print('Study/Work hour is not normal')
        return study_hours

    def get_valid_explanation(self):
        """get valid user explanation report (max 60 character)"""
        print('Explain in 60 character what did you do?')
        while True:
            print('Line shows 60 chracter length')
            print('*' * 60)
            explanation = input().strip()
            if len(explanation) <= 60:
                break
            else:
                print('WARNING: your explanation is too long')
        return explanation

    def clear_screen(self):
        os.system('cls' if os.__name__ == 'nt' else 'clear')


if __name__ == '__main__':
    try:
        TenTousandHours()
        Achievement()
    except KeyboardInterrupt:
        os._exit(1)
