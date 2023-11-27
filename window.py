import threading
import PySimpleGUI as sg
from DataManagement.DataController import DataControl
from datetime import date, datetime
import EmailTimer
  #Made by Chris Athanasi
sg.theme('DarkGrey5')

# Define functions to handle "Clock In" and "Clock Out" button clicks
def clock_in_action():
    first_name = window['first_name_input'].get()
    last_name = window['last_name_input'].get()
    data_control = DataControl()

    current_date = date.today()  # Today's date
    current_time = datetime.now().strftime("%I:%M %p")  # Current time

    # Write to both daily and weekly time card files
    if data_control.createFile(daily=True):
        data_control.writeToFile(first_name, last_name, current_time, "", current_date)
    if data_control.createFile(daily=False):
        data_control.writeToFile(first_name, last_name, current_time, "", current_date)

    sg.popup(f"Welcome: {first_name} ")
    print(f"Clock In: {first_name} {last_name}, Date: {current_date}, Time In: {current_time}")

def clock_out_action():
    first_name = window['first_name_input'].get()
    last_name = window['last_name_input'].get()
    current_time = datetime.now().strftime("%I:%M %p")

    data_control = DataControl()

    # Append clock out time to both daily and weekly time card files
    daily_filename = data_control.getDailyFileName()
    weekly_filename = data_control.getFileName()
    data_control.appendClockOut(daily_filename, first_name, last_name, current_time)
    data_control.appendClockOut(weekly_filename, first_name, last_name, current_time)

    if data_control.row_found:
        sg.popup("Thanks for clocking out, enjoy your day!")
    else:
        sg.popup("Name not found. Check for typos.")

    print(f"Clock Out: {first_name} {last_name}, Time Out: {current_time}")

input_layout = [[sg.Text('First Name:'), sg.InputText(key='first_name_input')], [sg.Text('Last Name:'), sg.InputText(key='last_name_input')]]
button_layout = [[sg.Button('Clock In', size=(10, 1))], [sg.Button('Clock Out', size=(10, 1))]]
column_layout = [[sg.Column(input_layout, vertical_alignment='center', justification='center', size=(300, 200))], [sg.Column(button_layout, vertical_alignment='center', justification='center', size=(100, 100))]]

window = sg.Window('Time Clock', column_layout, size=(400, 300))


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    if event == 'Clock In':
        clock_in_action()
    elif event == 'Clock Out':
        clock_out_action()

window.close()
