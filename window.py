import threading
import PySimpleGUI as sg
from DataManagement.DataController import DataControl
from datetime import date, datetime
import EmailTimer
    # ============= STATE MACHINE CLASS WILL FO HERE. ==============


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
    
    # Define functions to handle "Clock In" and "Clock Out" button clicks
    def clock_in_action():
        first_name = window['first_name_input'].get()
        # Checks to make sure the name is Characters, returns a True/False value. 
        print(first_name.isalpha())
        last_name = window['last_name_input'].get()
        data_control = DataControl()

        current_date = date.today()  # Today's date
        current_time = datetime.now().strftime("%I:%M %p")  # Current time

        # Write clock in time to both daily and weekly time card files
        data_control.writeToFile(first_name, last_name, current_time, "", current_date)
        
        
        sg.popup(f"Welcome: {first_name} ")
        print(f"Clock In: {first_name} {last_name}, Date: {current_date}, Time In: {current_time}")
        
        # Checks to see if user is clocked in, is not change the status. 
        if not STATUS.IsClockIn:
            STATUS.ChangeClockIn()
            print(f'Is clocked in. {STATUS.IsClockIn}. Is on break {STATUS.IsOnBreak}')

    def break_action():
        first_name = window['first_name_input'].get()
        last_name = window['last_name_input'].get()
        data_control = DataControl()

        current_date = date.today()
        current_time = datetime.now().strftime("%I:%M %p")

        # Record the break time
        data_control.recordBreak(first_name, last_name, current_date, current_time)

        sg.popup("Break recorded.")
        print(f"Break: {first_name} {last_name}, Date: {current_date}, Time: {current_time}")
        
        if not STATUS.IsOnBreak:
            STATUS.ChangeOnBreak()
            print(f'Is clocked in. {STATUS.IsClockIn}. Is on break {STATUS.IsOnBreak}')


    def clock_out_action():
        first_name = window['first_name_input'].get()
        last_name = window['last_name_input'].get()
        
        # ======================= UNIT TESTING FOR FIRST AND LAST NAME GOES HERE ================= # 
        
        data_control = DataControl()

        current_date = date.today()  # Today's date
        current_time = datetime.now().strftime("%I:%M %p") # Current time

        # Write clock out time to both daily and weekly time card files
        data_control.writeToFile(first_name, last_name, "", current_time, current_date)
        
        sg.popup("Thanks for clocking out, enjoy your day!")
        print(f"Clock Out: {first_name} {last_name}, Date: {current_date}, Time Out: {current_time}")
        
        if STATUS.IsClockIn:
            STATUS.ChangeClockIn()
            print(f'Is clocked in. {STATUS.IsClockIn}. Is on break {STATUS.IsOnBreak}')

    # ============ LOGO IMAGE GOES HEREE =============
    # ============ IF PERMISSABLE, STATUS IDICATOR =============

    input_layout = [[sg.Text('First Name:'), sg.InputText(key='first_name_input')],
                    [sg.Text('Last Name:'), sg.InputText(key='last_name_input')]]
    button_layout = [
        [sg.Button('Clock In', size=(10, 1))],
        [sg.Button('Clock Out', size=(10, 1))],
        [sg.Button('Break In/Out', size=(10, 1))]
    ]
    column_layout = [[sg.Column(input_layout, vertical_alignment='center', justification='center', size=(300, 150))],
                    [sg.Column(button_layout, vertical_alignment='center', justification='center', size=(100, 100))]]

    window = sg.Window('Time Clock', column_layout, size=(400, 300))

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        
        # Additional Logic to action listener.  Clock in button won't activate if user is already clocked in, and use can't clock out if they're on break. 
        
        if event == 'Clock In' and not STATUS.IsClockIn:
            clock_in_action()
        elif event == 'Clock Out' and STATUS.IsClockIn and not STATUS.IsOnBreak:
            clock_out_action()
        elif event == 'Break In/Out' and STATUS.IsClockIn: 
            break_action()

    window.close()
