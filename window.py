import threading
import PySimpleGUI as sg
from DataManagement.DataController import DataControl
from datetime import date, datetime
import EmailTimer

def main():
    # Made by Chris Athanasi
    sg.theme('DarkGrey5')
    
    # ============= STATE MACHINE CLASS WILL GO HERE. ==============

    # Define functions to handle "Clock In" and "Clock Out" button clicks
    def clock_in_action():
        first_name = window['first_name_input'].get()
        last_name = window['last_name_input'].get()
        data_control = DataControl()

        current_date = date.today()  # Today's date
        current_time = datetime.now().strftime("%I:%M %p")  # Current time

        # Write clock in time to both daily and weekly time card files
        data_control.writeToFile(first_name, last_name, current_time, "", current_date)
        
        
        sg.popup(f"Welcome: {first_name} ")
        print(f"Clock In: {first_name} {last_name}, Date: {current_date}, Time In: {current_time}")

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

    # ============ LOGO IMAGE GOES HEREE =============
    # ============ IF PERMISSABLE, STATUS IDICATOR =============
    logo_layout = [
    [sg.Image(filename='path_to_your_logo.png', key='logo')],
    [sg.Text('If Permissible, Status Indicator')]
    ]
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
        # ============= STATE MACHINE IN ADDITION TO THE EVENT LISTENER ===============
        if event == 'Clock In':
            clock_in_action()
        elif event == 'Clock Out':
            clock_out_action()
        elif event == 'Break In/Out': 
            break_action()

    window.close()
