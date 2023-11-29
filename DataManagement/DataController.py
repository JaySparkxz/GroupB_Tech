from datetime import date, datetime, timedelta
import csv
import os

class DataControl:
    currentWeek = date.today().isocalendar()[1]
    currentDate = date.today()

    def createFile(self, daily=False, filename=None, mode='a'):
        try:
            folder_name = "Daily Time Cards" if daily else "Weekly Time Cards"
            if filename is None:
                filename = f"Daily_Time_Card_{self.currentDate}.csv" if daily else f"Week_{self.currentWeek}.csv"

            header = ['First Name', 'Last Name', 'Time In', 'Time Out', 'Break Start', 'Break End', 'Date'] if daily else ['First Name', 'Last Name', 'Date', 'Total Work Time']
            full_path = os.path.join(folder_name, filename)
            print(f"Attempting to create file: {full_path}") 
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            file_exists = os.path.exists(full_path)
            with open(full_path, mode, newline='') as file:
                writer = csv.writer(file)

                if not file_exists:
                    writer.writerow(header)
                    print(f"CSV file '{filename}' created successfully in the '{folder_name}' folder.")
                else:
                    print(f"Appending to existing CSV file '{filename}'.")

            return True

        except Exception as e:
            print(f"Failed to create or append to CSV file: {e}")
            return False

    def calculateWorkTime(self, timeIn, timeOut, breakStart, breakEnd):
        time_format = "%I:%M %p"
        work_duration_minutes = 0

        # Validate timeIn and timeOut
        if timeIn and timeOut:
            try:
                start = datetime.strptime(timeIn, time_format)
                end = datetime.strptime(timeOut, time_format)
                duration = end - start
                work_duration_minutes = duration.total_seconds() / 60  # Convert to minutes
            except ValueError:
                return 0

        # Validate breakcStart and breakcEnd
        if breakStart and breakEnd:
            try:
                start_break = datetime.strptime(breakStart, time_format)
                end_break = datetime.strptime(breakEnd, time_format)
                break_duration = end_break - start_break
                break_duration_minutes = break_duration.total_seconds() / 60  # Convert to minutes
                work_duration_minutes -= break_duration_minutes
            except ValueError:
                pass  # Ignore break time calculation if invalid

        # Convert minutes to hours (with decimal part)
        total_work_hours = round(work_duration_minutes / 60, 2)

        return total_work_hours


    def writeToFile(self, firstName, lastName, timeIn, timeOut, date):
        # Daily time card entry
        self.updateOrWriteEntry(firstName, lastName, timeIn, timeOut, date, daily=True)

        # Weekly time card update
        if timeOut:  # Only update the weekly time card if clocking out
            self.updateOrWriteEntry(firstName, lastName, timeIn, timeOut, date, daily=False)

    def updateOrWriteEntry(self, firstName, lastName, timeIn, timeOut, date, daily):
        filename = self.getDailyFileName() if daily else self.getFileName()
        full_path = os.path.join("Daily Time Cards" if daily else "Weekly Time Cards", filename)

        if not os.path.exists(full_path):
            self.createFile(daily=daily, filename=filename)

        with open(full_path, 'r+', newline='') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

            updated = False
            for row in rows:
                if row['First Name'] == firstName and row['Last Name'] == lastName and row['Date'] == str(date):
                    if daily:
                        # Update daily time card entry
                        if timeOut:
                            row['Time Out'] = timeOut
                        updated = True
                    else:
                        # Calculate and update weekly time card entry
                        totalWorkTime = self.calculateWorkTime(timeIn, timeOut, '', '')
                        row['Total Work Time'] = str(float(row.get('Total Work Time', 0)) + totalWorkTime)
                        updated = True
                    break

            file.seek(0)
            file.truncate()
            writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(rows)

            if not updated:
                # Append new entry if not updated
                totalWorkTime = self.calculateWorkTime(timeIn, timeOut, '', '') if not daily else 0
                new_row = [firstName, lastName, str(date), totalWorkTime] if not daily else [firstName, lastName, timeIn, timeOut, '', '', str(date)]
                writer = csv.writer(file)
                writer.writerow(new_row)






    def recordBreak(self, firstName, lastName, date, breakTime):
        filename = self.getDailyFileName()
        full_path = os.path.join("Daily Time Cards", filename)

        if not os.path.exists(full_path):
            self.createFile(daily=True, filename=filename)

        with open(full_path, 'r+', newline='') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

            break_updated = False
            for row in rows:
                if row['First Name'] == firstName and row['Last Name'] == lastName and row['Date'] == str(date):
                    # If there is a break start but no break end, record break end
                    if row['Break Start'] and not row['Break End']:
                        row['Break End'] = breakTime
                        break_updated = True
                        break
                    # If there is no break start, record break start
                    elif not row['Break Start']:
                        row['Break Start'] = breakTime
                        break_updated = True
                        break

            file.seek(0)
            file.truncate()
            writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(rows)

            if not break_updated:
                # If no break entry was updated, append a new entry with only break start time
                with open(full_path, 'a', newline='') as file_append:
                    writer = csv.writer(file_append)
                    writer.writerow([firstName, lastName, "", "", breakTime, "", str(date)])

    def getFileName(self):
        filename = f"Week_{self.currentWeek}.csv"
        print(f"Weekly file name: {filename}")
        return filename

    def getDailyFileName(self):
        return f"Daily_Time_Card_{str(self.currentDate)}.csv"
    
  

    @staticmethod
    def test_weekly_accumulation():
        # Simulate a week's clock-ins and clock-outs
        work_days = [
            ("09:00 AM", "05:00 PM"),  # Monday
            ("09:30 AM", "05:30 PM"),  # Tuesday
            ("10:00 AM", "06:00 PM"),  # Wednesday
            ("09:00 AM", "05:00 PM"),  # Thursday
            ("09:30 AM", "04:30 PM")   # Friday
        ]

        
        current_weekday = date.today().weekday()
        monday = date.today() - timedelta(days=current_weekday)
        data_control = DataControl()

        # Testing for each day
        for i, (time_in, time_out) in enumerate(work_days):
            test_date = monday + timedelta(days=i)
            date_str = test_date.strftime("%Y-%m-%d")
            data_control.writeToFile("John", "Doe", time_in, time_out, date_str)
            data_control.writeToFile("Elton", "Jon", time_in, time_out, date_str)

            # Print the weekly time card content
            weekly_file = data_control.getFileName()
            full_weekly_path = os.path.join("Weekly Time Cards", weekly_file)
            print(f"Checking weekly file at: {full_weekly_path}")  # Diagnostic print
            print(f"Current working directory: {os.getcwd()}")

            if os.path.exists(weekly_file):
                print(f"\nContents of {weekly_file} after day {i+1} (Date: {date_str}):")
                with open(weekly_file, 'r') as file:
                    print(file.read())
            else:
                print(f"Weekly file {full_weekly_path} not found.")

    def getEmailBody(self, filename, folder):
        """Reads the content of a CSV file and returns it as a string."""
        try:
            full_path = os.path.join(folder, filename)
            with open(full_path, 'r') as file:
                content = file.read()
            return content
        except Exception as e:
            print(f"Error while reading the file: {e}")
            return ""
        
  






# Example usagedata_control = DataControl()

# Creating a weekly time card file
data_control.createFile()


# Creating a daily time card file for today's date
data_control.createFile(daily=True)
#To run a test just remove this uncomment the method call below
##data_control.test_weekly_accumulation()





