import threading
import PySimpleGUI as sg
from DataManagement.DataController import DataControl
from datetime import date, datetime
import EmailTimer

# ============= STATE MACHINE CLASS WILL GO HERE. ==============

def main():
    # Made by Chris Athanasi
    sg.theme('DarkGrey5')
    class ClockInStatus():
        def __init__(self,):
            self.IsClockIn = False
            self.IsOnBreak = False
        def ChangeClockIn(self):
            self.IsClockIn = not self.IsClockIn
            print(self.IsClockIn)
        def ChangeOnBreak(self):
            self.IsOnBreak = not self.IsOnBreak

    STATUS = ClockInStatus()

    def validate_names(first_name, last_name):
    # Check if first_name and last_name only contain uppercase letters, lowercase letters, or hyphens
        if all(char.isalpha() or char == '-' for char in first_name) and all(char.isalpha() or char == '-' for char in last_name):
            return True
        else:
            sg.popup("Invalid characters in First Name or Last Name. Do not use numbers or symbols.")
            print("Invalid characters in First Name or Last Name. Do not use numbers or symbols.")
            return False


        
    # Define functions to handle "Clock In" and "Clock Out" button clicks
    def clock_in_action():
        first_name = window['first_name_input'].get()
        last_name = window['last_name_input'].get()

        # Validate names before proceeding
        if not validate_names(first_name, last_name):
            return

        data_control = DataControl()

        current_date = date.today()  # Today's date
        current_time = datetime.now().strftime("%I:%M %p")  # Current time

        # Write clock in time to both daily and weekly time card files
        data_control.writeToFile(first_name, last_name, current_time, "", current_date)

        sg.popup(f"Welcome: {first_name} ")
        print(f"Clock In: {first_name} {last_name}, Date: {current_date}, Time In: {current_time}")

        # Checks to see if the user is clocked in, is not change the status.
        if not STATUS.IsClockIn:
            STATUS.ChangeClockIn()
            print(f'Is clocked in. {STATUS.IsClockIn}. Is on break {STATUS.IsOnBreak}')

        

    def break_action():
        first_name = window['first_name_input'].get()
        last_name = window['last_name_input'].get()

        # Validate names before proceeding
        if not validate_names(first_name, last_name):
            return

        data_control = DataControl()

        current_date = date.today()
        current_time = datetime.now().strftime("%I:%M %p")

        # Record the break time
        data_control.recordBreak(first_name, last_name, current_date, current_time)

        sg.popup("Break recorded.")
        print(f"Break: {first_name} {last_name}, Date: {current_date}, Time: {current_time}")

        STATUS.ChangeOnBreak()
        print(f'Is clocked in. {STATUS.IsClockIn}. Is on break {STATUS.IsOnBreak}')

    def clock_out_action():
        first_name = window['first_name_input'].get()
        last_name = window['last_name_input'].get()

        # Validate names before proceeding
        if not validate_names(first_name, last_name):
            return

        data_control = DataControl()

        current_date = date.today()  # Today's date
        current_time = datetime.now().strftime("%I:%M %p")  # Current time

        # Write clock out time to both daily and weekly time card files
        data_control.writeToFile(first_name, last_name, "", current_time, current_date)

        sg.popup("Thanks for clocking out, enjoy your day!")
        print(f"Clock Out: {first_name} {last_name}, Date: {current_date}, Time Out: {current_time}")

        if STATUS.IsClockIn:
            STATUS.ChangeClockIn()
            print(f'Is clocked in. {STATUS.IsClockIn}. Is on break {STATUS.IsOnBreak}')

        

    # ============ IF PERMISSIBLE, STATUS INDICATOR =============
    def get_file_name():
        if STATUS.IsOnBreak:
            return './Assets/OBDark.png'
        else:
            if STATUS.IsClockIn:
                return './Assets/CIDark.png'
            else:
                return './Assets/CODark.png'

    input_layout = [
        [sg.Text('First Name:'), sg.InputText(key='first_name_input')],
        [sg.Text('Last Name:'), sg.InputText(key='last_name_input')],
    ]

    button_layout = [
        [sg.Button('Clock In', size=(10, 1))],
        [sg.Button('Clock Out', size=(10, 1))],
        [sg.Button('Break In/Out', size=(10, 1))]
    ]

    top_row_layout = [
        [sg.Column(input_layout),],
        # logo_layout = [     [sg.Image(filename='add path to logo here', key='logo png name')],
    ]
    middle_row_layout = [
        [sg.Image(filename=get_file_name(), size=(300, 150), key='-IMAGE-')]
    ]

    bottom_row_layout = [
        [sg.Image(filename='./Assets/MCCLOGO.PNG', key='logo'), sg.Column(button_layout)],
    ]

    window_layout = [
        [sg.Column(top_row_layout, vertical_alignment='center', justification='center', size=(300, 100), pad=20)],
        [sg.Column(middle_row_layout, vertical_alignment='center')],
        [sg.Column(bottom_row_layout, vertical_alignment='center', justification='center')],
    ]

    window = sg.Window('Time Clock', window_layout, icon="Assets/TimeClockLogo.ico")

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break

        # Additional Logic to action listener. Clock in button won't activate if the user is already clocked in,
        # and the user can't clock out if they're on break.

        if event == 'Clock In' and not STATUS.IsClockIn:
            clock_in_action()
        elif event == 'Clock Out' and STATUS.IsClockIn and not STATUS.IsOnBreak:
            clock_out_action()
        elif event == 'Break In/Out' and STATUS.IsClockIn:
            break_action()
            # Update window with a new image
        window['-IMAGE-'].update(filename=get_file_name())

    window.close()
