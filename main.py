import tkinter as tk
import datetime

class Application(tk.Frame):
    # initializes the window frame
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
    # A function to display the date on the console.
    # Format YYYY-MM-DD HH:MM:SS:?????
    def printTime(self):
        print(datetime.datetime.now())

    # Creates a button that runs the printTime function when clicked
    def createWidgets(self):
        self.Button = tk.Button(self, text='Print Time',
            command=self.pTime)
        self.Button.grid()


# Keeps the application running.
app = Application()
app.master.title('Sample application')
app.mainloop()