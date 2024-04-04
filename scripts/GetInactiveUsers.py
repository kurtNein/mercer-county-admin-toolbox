import arcpy
from arcgis.gis import GIS
from datetime import datetime, timedelta
import time
import pandas as pd

arcpy.AddMessage("ArcGIS Online Org account")
gis = GIS('home')
arcpy.AddMessage("Logged in as " + str(gis.properties.user.username))


def construct_grace_period_date(days=60):
    current_time_struct = time.localtime()

    # Convert time.struct_time object to a datetime object
    current_datetime = datetime.fromtimestamp(time.mktime(current_time_struct))

    # Subtract days
    new_datetime = current_datetime - timedelta(days)

    # Convert back to time.struct_time object
    new_time_struct = new_datetime.timetuple()
    return new_time_struct


def get_inactive_users(log_csv_path: str, search_user='*'):
    from arcgis import GIS
    import csv
    import time

    output_csv = r'..\outputs\users.csv'  # change
    search_user = '*'  # change to query individual user

    GRACE_PERIOD_DAYS = 90

    gis = GIS('home')

    user_list = gis.users.search(query=search_user, max_users=1000)

    with open(output_csv, 'w', encoding='utf-8') as file:
        csvfile = csv.writer(file, delimiter=',', lineterminator='\n')
        csvfile.writerow(
            ["Name",  # these are the headers; modify according to whatever properties you want in your report
             "LastLogOn"
             ])

        for item in user_list:
            if item.lastLogin != -1 and time.localtime(item.lastLogin / 1000) < construct_grace_period_date(GRACE_PERIOD_DAYS):
                csvfile.writerow([item.username,  # modify according to whatever properties you want in your report
                                  time.strftime('%m/%d/%Y', time.localtime(item.lastLogin / 1000))
                                  ])

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(output_csv, names=['Name', 'LastLogOn'])

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        try:
            # Access each column value using the column name
            column1_value = row['Name']
            column2_value = row['LastLogOn']

            minimum_logon_date = datetime.now() - timedelta(days=GRACE_PERIOD_DAYS)

            if datetime.strptime(column2_value, "%m/%d/%Y") < minimum_logon_date:
                print(f"Row {index + 1}: {column1_value}, {column2_value}")
        except Exception as e:
            print(e)


if __name__ == '__main__':
    get_inactive_users('')
