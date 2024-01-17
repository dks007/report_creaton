import math

import pandas as pd
import mysql.connector
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "success_tool.settings")

import django
django.setup()

from django.contrib.auth.models import User
db_host = 'localhost'
db_user = 'root'
db_password = 'test'
db_name = 'ifsreporting_local'
mysql_config = {
    'host': db_host,
    'user': db_user,
    'password': db_password,
    'database': db_name,
}

# Excel file path and sheet name
excel_file_path = '/home/rafique/Desktop/reporting/apps/utility/data_mapping_1.xlsx'
sheet_name = 'menu_sdo'
table_name = 'dashboard_sdomaster'

# Connect to MySQL
conn = mysql.connector.connect(**mysql_config)
cursor = conn.cursor()

# Read Excel file into a pandas DataFrame
df = pd.read_excel(excel_file_path, sheet_name=sheet_name)

# Iterate through DataFrame rows and insert into the database
for index, row in df.iterrows():
    # print(index, " >>>> ", row[0])
    # success_service_name = row[5]  # row index need to insert
    # customer_id = row[3] #if len(row) > 2 and row[2] is not None else 'NA'
    # customer_id = row[2]
    sdo_name = row[1]
    sdo_email = 'NA'
    # template_file_name = row[2]
    # if isinstance(success_service_name, float) and math.isnan(success_service_name):
    #     success_service_name = 'NA'
    # elif success_service_name == 'nan':
    #     success_service_name = 'NA'

    # print(csm_name)
    # menu_description = row[1]
    # template_file_name = row[2]
    # template_file_path = 'file_path'
    # template_file_type = 'xlsx'
    # template_file_size = 1

    # print(industry_type_name, '>>>>>>>>>', industry_description)

    # if csm_name is None or csm_name == '':
    #     continue


    # Assuming your table has columns named col1, col2, col3
    sql = f"INSERT INTO {table_name} (sdo_name, sdo_email, created_date, updated_date, status) VALUES (%s, %s, CURDATE(), CURDATE(), 1)"

    try:
        cursor.execute(sql, (sdo_name, sdo_email))
        conn.commit()
        print("Record inserted successfully")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Close MySQL connection
cursor.close()
conn.close()
