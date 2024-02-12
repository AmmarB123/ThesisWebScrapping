import weekday
import os
import datetime
import pytz
'''
This function is used to check the current day in comparison to the day in the database
It is used to refresh the masterdata excel sheet 
'''
def day():



    # Gets the timezone in lodnon
    tz = pytz.timezone('Europe/London')
    # Gets the current day time of your device
    current_datetime = datetime.datetime.now(tz)
    # Gets the day of the week as an integer
    day_of_week = current_datetime.weekday()


    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    # Gets the string value of the day by using the index
    weekday_name = weekdays[day_of_week]


    # Selects the weekday in the weekday.db
    weekday_check = "SELECT weekday FROM WEEKDAY WHERE weekday = ?"
    # Connection
    cur1 = weekday.connect.cursor()
    # Check if it is same
    cur1.execute(weekday_check, (weekday_name,))
    # Gets the result
    result1 = cur1.fetchone()
    # If the result is the same it will be valid other wise updated the table with the new weekday and delete the master data
    if result1 is not None:
        print('valid')
    else:
        cur1.execute("UPDATE WEEKDAY SET WEEKDAY = ? WHERE ID = 1", (weekday_name,))
        print("enter")
        try:
            os.remove('masterdata.xlsx')
        except:
            pass


    weekday.connect.commit()

