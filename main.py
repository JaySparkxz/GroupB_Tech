import tkinter as tk
import datetime

class Application(tk.Frame):
    # initializes the window frame
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
    
    # A function to display the date on the console.
    # Format YYYY-MM-DD HH:MM:SS
    def printTime(self):
        current_time = datetime.datetime.now()
        # This line blwo cuts off the decimals that were present in the original code
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
        print(formatted_time)

    # Creates a button that runs the printTime function when clicked
    def createWidgets(self):
        self.Button = tk.Button(self, text='Print Time',
            command=self.printTime)
        self.Button.grid()


# Keeps the application running.
app = Application()
app.master.title('Sample application')
app.mainloop()
