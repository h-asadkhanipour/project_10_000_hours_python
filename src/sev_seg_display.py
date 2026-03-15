class SevSeg:
    def __init__(self, number_1, number_2=None, number_3=None, number_4=None, separator=None):
        # add numbers to a list
        self.displayed_number_list = []
        if number_1:
            self.displayed_number_list.append(number_1)
        if number_2:
            self.displayed_number_list.append(number_2)
        if number_3:
            self.displayed_number_list.append(number_3)
        if number_4:
            self.displayed_number_list.append(number_4)
        self.separator = separator
        if self.separator == None:
            self.separator = '  '
        self.final_line_1 = []
        self.final_line_2 = []
        self.final_line_3 = []
        for number in self.displayed_number_list:
            if not self.check_valid_number(number):
                print(f'Number {number} is not valid')
                print(f'This number:{number} is removed')
                self.displayed_number_list.remove(number)
        for number in self.displayed_number_list:
            if len(str(number)) > 15:
                print('Number should be less than 16 digits')
                print(f'This {number} is removed')
                self.displayed_number_list.remove(number)
        for number in self.displayed_number_list:
            self.add_numbers_to_sevseg_lines(number)
        self.final_print()

    def check_valid_number(self, number):
        """checks if input number is valid, 
        if number is integer of string of an integer returns True"""
            
        if isinstance(number, int) or number.isdigit():
            return True
        return False
    
    def add_numbers_to_sevseg_lines(self, number):
        list_num = list(str(number))
        list_num = [int(i) for i in list_num]

        line_1 = {
            1: '    ',
            2: ' __ ',
            3: ' __ ',
            4: '    ',
            5: ' __ ',
            6: ' __ ',
            7: ' __ ',
            8: ' __ ',
            9: ' __ ',
            0: ' __ ',
        }

        line_2 = {
            1: '   |',
            2: ' __|',
            3: ' __|',
            4: '|__|',
            5: '|__ ',
            6: '|__ ',
            7: '   |',
            8: '|__|',
            9: '|__|',
            0: '|  |',
        }

        line_3 = {
            1: '   |',
            2: '|__ ',
            3: ' __|',
            4: '   |',
            5: ' __|',
            6: '|__|',
            7: '   |',
            8: '|__|',
            9: ' __|',
            0: '|__|'
        }

        for i in list_num:
            self.final_line_1.append(line_1[i])
            self.final_line_1.append(' ') # this is space between each digit number in a row
            self.final_line_2.append(line_2[i])
            self.final_line_2.append(' ') # this is space between each digit number in a row
            self.final_line_3.append(line_3[i])
            self.final_line_3.append(' ') # this is space between each digit number in a row
        # add separator
        self.final_line_1.append('  ') # this is space between each digit number in a row
        self.final_line_2.append(f'{self.separator} ') # this is space between each digit number in a row
        self.final_line_3.append(f'{self.separator} ') # this is space between each digit number in a row
        

    def final_print(self):
        # remove last separator
        self.final_line_2.pop()
        self.final_line_3.pop()
        print(''.join(self.final_line_1))
        print(''.join(self.final_line_2))
        print(''.join(self.final_line_3))

if __name__ =='__main__':
    SevSeg(12, 34, 56, None, separator='*')