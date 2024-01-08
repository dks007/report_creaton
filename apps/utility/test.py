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
sheet_name = 'menu_cards'
table_name = 'dashboard_menucardmaster'

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
    menu_card = row[0]
    menu_description = row[1]
    template_file_name = row[2]
    template_file_path = 'file_path'
    template_file_type = 'xlsx'
    template_file_size = 1

    # print(industry_type_name, '>>>>>>>>>', industry_description)

    if menu_card is None or menu_card == '':
        continue


    # Assuming your table has columns named col1, col2, col3
    sql = f"INSERT INTO {table_name} (menu_card, menu_description, template_file_name, template_file_path, template_file_type, template_file_size, created_date, updated_date, status) VALUES (%s, %s, %s, %s, %s, %s, CURDATE(), CURDATE(), 1)"

    try:
        cursor.execute(sql, (menu_card, menu_description, template_file_name, template_file_path, template_file_type, template_file_size))
        conn.commit()
        print("Record inserted successfully")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Close MySQL connection
cursor.close()
conn.close()
