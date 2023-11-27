from datetime import date
import csv
import os

class DataControl:
    #Made by Chris Athanasi
    currentWeek = date.today().isocalendar()[1]  
   
    currentDate = date.today()  
    writer = None
    file = None
    row_found = None

    def createFile(self, daily=False, filename=None, mode='a'):
        try:
            folder_name = "Daily Time Cards" if daily else "Weekly Time Cards"
            if filename is None:
                filename = f"Daily_Time_Card_{self.currentDate}.csv" if daily else f"Week_{self.currentWeek}.csv"

            header = ['First Name', 'Last Name', 'Time In', 'Time Out', 'Date']
            full_path = os.path.join(folder_name, filename)

            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            file_exists = os.path.exists(full_path)
            self.file = open(full_path, mode, newline='')
            self.writer = csv.writer(self.file)

            if not file_exists:
                self.writer.writerow(header)
                print(f"CSV file '{filename}' created successfully in the '{folder_name}' folder.")
            else:
                print(f"Appending to existing CSV file '{filename}'.")
            return True

        except Exception as e:
            print(f"Failed to create or append to CSV file: {e}")
            return False

    def writeToFile(self, firstName, lastName, timeIn, timeOut, date):
        self.handleFileUpdate(firstName, lastName, timeIn, timeOut, date, daily=True)
        self.handleFileUpdate(firstName, lastName, timeIn, timeOut, date, daily=False)

    def handleFileUpdate(self, firstName, lastName, timeIn, timeOut, date, daily):
        filename = self.getDailyFileName() if daily else self.getFileName()
        full_path = os.path.join("Daily Time Cards" if daily else "Weekly Time Cards", filename)

        if not os.path.exists(full_path):
            self.createFile(daily=daily, filename=filename)

        with open(full_path, 'r+', newline='') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

            # Check for existing entry on the same day for the user
            entry_exists = any(row for row in rows if row['First Name'] == firstName and row['Last Name'] == lastName and row['Date'] == str(date))

            if not entry_exists:
                # Move to end of file to append a new entry
                file.seek(0, os.SEEK_END)
                writer = csv.writer(file)
                writer.writerow([firstName, lastName, timeIn, timeOut, str(date)])

    def appendClockOut(self, filename, firstName, lastName, clockOutTime):
        folder_name = "Daily Time Cards" if "Daily" in filename else "Weekly Time Cards"
        full_path = os.path.join(folder_name, filename)

        if not os.path.exists(full_path):
            self.createFile(daily="Daily" in filename, filename=filename)

        self.row_found = False
        try:
            with open(full_path, 'r+') as file:
                reader = csv.DictReader(file)
                rows = list(reader)

                for row in rows:
                    if row['First Name'].strip() == firstName and row['Last Name'].strip() == lastName and row['Date'] == str(self.currentDate) and row['Time Out'].strip() == '':
                        row['Time Out'] = clockOutTime
                        self.row_found = True
                        break

                if self.row_found:
                    file.seek(0)
                    file.truncate()
                    writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
                    writer.writeheader()
                    writer.writerows(rows)
                else:
                    print("No matching entry found for the name provided.")
        except Exception as e:
            print(f"Error while appending clock out time: {e}")

    def getEmailBody(self, filename):
        try:
            full_path = os.path.join("TimeCards", filename)
            with open(full_path, 'r') as file:
                reader = csv.reader(file)
                lines = list(reader)

            body = "Time Card Data:\n\n"
            for line in lines:
                body += ', '.join(line) + "\n"
            return body
        except Exception as e:
            print(f"Error while setting email body: {e}")
            return ""

    def getFileName(self):
        filename = f"Week_{self.currentWeek}.csv"
        return filename

    def getDailyFileName(self):
        filename = f"Daily_Time_Card_{str(self.currentDate)}.csv"
        return filename

    def closeFile(self):
        if self.file:
            self.file.close()






data_control = DataControl()

# Creating a weekly time card file
data_control.createFile()
data_control.closeFile()

# Creating a daily time card file for today's date
data_control.createFile(daily=True)
data_control.closeFile()


