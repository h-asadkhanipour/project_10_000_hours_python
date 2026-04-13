from datetime import datetime
from typing import Protocol


class InputValidation(Protocol):
    def validate(self, input):
        pass


class DateValidation():
    def validate(self, input):
        while True:
            try:
                input = datetime.strptime(input, "%Y/%m/%d").date()
                break
            except ValueError:
                print(f'{input} is not a valid date')
        return input


class HoursValidation():
    def validate(self, input):
        while True:
            try:
                float(input)
            except ValueError:
                print(f'{input} is not valid')
                continue

            if 0 <= float(input) <= 18:
                if float(input) % 0.5 == 0:
                    input = float(input)
                    break
                else:
                    print('Study/Work hour should be multiple of 0.5 (half hour)')
            else:
                print('Study/Work hour is not normal')
        return input


class ExplanationValidation():
    def validate(self, input):
        """get valid user explanation report (max 60 character)"""
        print('Explain in 60 character what did you do?')
        while True:
            print('Line shows 60 chracter length')
            print('*' * 60)
            input = input.strip()
            if len(input) <= 60:
                break
            else:
                print('WARNING: your explanation is too long')
        return input
