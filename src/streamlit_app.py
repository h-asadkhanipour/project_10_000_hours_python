
import subprocess
from datetime import datetime
from datetime import timedelta

import streamlit as st
import openpyxl


app_title ='''
# The idea is this:  
If you spend about **10,000 hours** practicing a skill in a focused, deliberate way, you can become **world-class** at it.  
> Malcolm Gladwell's book Outliers, based on research by psychologist "Anders Ericsson"
---  
10,000 hours ≈ 3 hours a day for 10 years  
It's not just doing something a lot — it's practicing with intention, pushing your limits.  
'''


about_me = '''
Contact [me](www.github.com/h-asadkhanipour)
'''


class TenThousandHoursPython:
    def __init__(self):
        self.today = datetime.today()
        self.years = [i for i in range(self.today.year, self.today.year + 5)]
        try:
            self.excel_file = openpyxl.load_workbook('data/daily_time_log.xlsx')
            print('Reports Excel file loaded')
        except FileNotFoundError:
            dirs = subprocess.check_output('ls -d */', shell=True, text=True)
            if 'data/' not in dirs:
                subprocess.run(['mkdir', 'data/'])
            self.excel_file = self.create_workbook()
            self.excel_file.save('data/daily_time_log.xlsx')
            print('New reports Excel file created')
        self.excel_file.save('data/daily_time_log.xlsx')
    
    def achievement(self):
        years = self.years
        self.first_day = None
        # calculate for each year
        achievement_hours = 0   # accumolates after each year iteration
        self.total_days = 0          # accumolates after each year iteration
        for year in years:
            sheet = self.excel_file[f'{year}_report']
            non_empty_cells = []
            # find non-empty cells
            for i in range(2, 368):
                if sheet[f'B{i}'].value != None and sheet[f'B{i}'].value >= 0:
                    non_empty_cells.append(i)
            if non_empty_cells:      
                first_report_day = min(non_empty_cells)
                last_report_day = max(non_empty_cells)
                for day in range(first_report_day, last_report_day + 1):
                    if sheet[f'B{day}'].value == None:
                        sheet[f'B{day}'] = 0
                    self.total_days += 1
                    achievement_hours += sheet[f'B{day}'].value
                if self.first_day == None:                          # find first report day
                    self.first_day = sheet[f'A{first_report_day}'].value
            sheet['F1'] = achievement_hours                         # achievement hours
            sheet['F2'] = (achievement_hours /10_000) * 100         # achievement percent
            sheet['F3'] = (achievement_hours / self.total_days)          # mean hours per day
            sheet['F4'] = 10_000 - achievement_hours                # hours to end
            sheet['F5'] = sheet['F4'].value / sheet['F3'].value     # days to end
            sheet['F6'] = sheet['F5'].value / 7                     # weeks to end
            sheet['F7'] = sheet['F5'].value / 30                    # months to end
            sheet['F8'] = sheet['F5'].value / 365                   # years to end
            # if this year achieve move hours, then recalculate celebration day
            if year == years[0]:
                sheet['F9'] = (sheet[f'A{last_report_day}'].value + timedelta(sheet['F5'].value)).date()  # last celebration day based on accumolated hours
            elif self.excel_file[f'{year}_report']['F1'].value > self.excel_file[f'{year - 1}_report']['F1'].value:
                sheet['F9'] = (sheet[f'A{last_report_day}'].value + timedelta(sheet['F5'].value)).date()  # last celebration day based on accumolated hours
            else:
                sheet['F9'] = self.excel_file[f'{year - 1}_report']['F9'].value
        self.achievement_hours = achievement_hours
        self.achievement_percent = (achievement_hours /10_000) * 100
        self.mean_hours_per_day = (achievement_hours / self.total_days)
        self.hours_to_end = 10_000 - achievement_hours
        self.days_to_end = self.hours_to_end / self.mean_hours_per_day
        self.weeks_to_end = self.days_to_end / 7
        self.months_to_end = self.days_to_end / 30
        self.years_to_end = self.days_to_end / 365
        self.celebration_day = self.excel_file[f'{max(years)}_report']['F9'].value # last year, last result
        self.excel_file.save('data/daily_time_log.xlsx')

    def get_user_input(self, study_hours, explanation):
        self.study_hours = float(study_hours)
        self.explanation = explanation
    
    def today_report(self):
        # find excel cell according to today and update its time
        sheet = self.excel_file[f'{self.today.year}_report']
        for cell in range(2,368):
            if str(self.today.date()) in str(sheet[f'A{cell}'].value):
                # if study hour is None , new value assign to it, else add to previous one 
                if sheet[f'B{cell}'].value == None:
                    sheet[f'B{cell}'] = float(self.study_hours)
                else:
                    sheet[f'B{cell}'] = sheet[f'B{cell}'].value + float(self.study_hours)
                sheet[f'C{cell}'] = self.explanation
        self.excel_file.save('data/daily_time_log.xlsx')

    def create_workbook(self):
        # create a new workbook
        excel_file = openpyxl.Workbook()
        # delete defualt sheet
        del excel_file['Sheet']
        # create five years from today
        years = self.years
        # default values of some cells in each sheet    
        cells = {
            'A1': 'date',
            'B1': 'study_work_hours',
            'C1': 'explanation',
            'E1': 'achievement_hours',
            'E2': 'achievement_percent',
            'E3': 'mean_hours_per_day',
            'E4': 'hours_to_end',
            'E5': 'days_to_end',
            'E6': 'weeks_to_end',
            'E7': 'months_to_end',
            'E8': 'years_to_end',
            'E9': 'celbration_day',
        }

        for year in years:
            excel_file.create_sheet(f'{year}_report')
            # change some cells to default values
            for cell, value in cells.items():
                excel_file[f'{year}_report'][cell] = value
            # find if year is leap year or not
            if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
                num_of_days = 366
            else:
                num_of_days = 365
            # create days of each year in A2:A366 or A2:A367 if year is leap
            for day in range(1, num_of_days + 1):
                # first access each sheet based on upper loop
                # then access each day cell based on this loop
                # asign datetime result to each cell
                # timedelta is -1 because start should be first day of year
                excel_file[f'{year}_report'][f'A{day + 1}'] = datetime(year=year, month=1, day=1) + timedelta(days=day - 1) 
        return excel_file


def get_valid_user_input():
    # get valid study hours for today
    # if you enter several time, you study hour will increase and explanation would be replaced
    try:
        study_hours = st.text_input('How much did you study/work Python today? ')
        if 0<= float(study_hours) <= 18:
            if float(study_hours) % 0.5 == 0:
                st.success('Study/Work hours is valid')
            else:
                st.error('Study/Work hour should be multiple of 0.5 (half hour)')
        else:
            st.error('Study/Work hour is not normal')
    except ValueError:
        st.error('Enter a number')

    # get valid user explanation report (max 60 character)
    explanation = st.text_input('Explain in 60 character what did you do today?')
    if 0 < len(explanation) <= 60:
        st.success('Explanation is valid')
    else:
        st.error('Explanation should be  less than 60 chatacters')
    try:
        if explanation != '':
            obj.get_user_input(study_hours, explanation)
            obj.today_report()
            obj.achievement()
            st.success('Today\'s report updated')
    except ValueError:
        st.error('Enter valid Study/Work hours')


try:
    obj = TenThousandHoursPython()
    obj.achievement()
    progress = obj.achievement_percent / 100
except ZeroDivisionError:
    st.write(app_title)
    st.sidebar.header(about_me)
    st.write('')
    st.write('')
    st.warning('This is your first day')
    st.warning('Ignore the errors, reload after you enter today\'s report')
    st.warning('Ignore the errors, reload after you enter today\'s report')
    get_valid_user_input()
    st.warning('Ignore the errors, reload after you enter today\'s report')
    st.warning('Ignore the errors, reload after you enter today\'s report')
    st.warning('This is your first day')


st.write(app_title)
st.sidebar.header(about_me)
st.write('')
st.write('')
get_valid_user_input()
st.write('')
st.write('')
st.write('Your progrss is:')
col1, col2 = st.columns(2)
with col1:
    st.progress(progress) 
with col2:
    st.write(f'{progress * 100:.0f} %')
st.write('You have achieved:', obj.achievement_hours, 'hours')
st.write('')
st.write('')
st.write('You have started this project in:', obj.first_day.date())
st.write('You have Studied/Worked for', obj.total_days, 'days')
st.write('Your mean Study/Work hours is:', obj.mean_hours_per_day)
st.write('')
st.write('')
st.write('Estimated days to achieve your goal:', obj.days_to_end, 'days')
st.write('Estimated weeks to achieve your goal:', obj.weeks_to_end, 'weeks')
st.write('Estimated months to achieve your goal:', obj.months_to_end, 'months')
st.write('Estimated years to achieve your goal:', obj.years_to_end, 'years')
st.write('Based on your average study hours, celebration day would be:' ,obj.celebration_day)

