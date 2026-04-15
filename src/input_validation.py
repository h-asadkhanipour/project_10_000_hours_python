from datetime import datetime
from typing import Protocol


class InputValidation(Protocol):
    def validate(self, msg):
        pass


class DateValidation():
    """Take a date string and check if data is valid or not"""

    def validate(self, msg):
        user_input = input(f'{msg}').lower().strip()
        while True:
            try:
                user_input = datetime.strptime(user_input, "%Y/%m/%d").date()
                break
            except ValueError:
                print(f'{user_input} is not a valid date')
                user_input = input(f'{msg}').lower().strip()
        return user_input


class HoursValidation():
    """Check study hours are multiple of 0.5 and less than 
    or equal to 18 hours"""

    def validate(self, msg):
        user_input = input(f'{msg}').lower().strip()
        while True:
            try:
                float(user_input)
            except ValueError:
                print(f'{user_input} is not valid')
                user_input = input(f'{msg}').lower().strip()
                continue

            if 0 <= float(user_input) <= 18:
                if float(user_input) % 0.5 == 0:
                    user_input = float(user_input)
                    break
                else:
                    print('Study/Work hour should be multiple of 0.5 (half hour)')
                    user_input = input(f'{msg}').lower().strip()
                    continue
            else:
                print('Study/Work hour is not normal')
                user_input = input(f'{msg}').lower().strip()
        return user_input


class ExplanationValidation():
    """get valid user explanation report (max 60 character)"""

    def validate(self, msg):
        print(msg)
        while True:
            print('Line shows 80 chracter length')
            print('*' * 80)
            user_input = input()
            if len(user_input) == 0:
                print('WARNING: provide some explanation')
                continue
            if 0 < len(user_input) < 80:
                break
            print('WARNING: your explanation is too long')
        return user_input


class YesNoValidation():
    """Ask user for yes/no, return True/False"""

    def validate(self, msg):
        user_input = input(f'{msg}').lower().strip()
        while True:
            if user_input in ['y', 'n', 'yes', 'no']:
                break
            user_input = input(f'{msg}').lower().strip()
        if user_input in ['y', 'yes']:
            return True
        return False
