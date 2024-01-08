from openpyxl import load_workbook
import pymysql

# Replace these with your MySQL database details
db_host = 'localhost'
db_user = 'root'
db_password = 'test'
db_name = 'ifsreporting_local'

# Replace this with the path to your Excel file
excel_file_path = '/home/rafique/Desktop/reporting/apps/utility/data_mapping_1.xlsx'

# Specify the sheet name you want to read
sheet_name = 'menu_sdo'

# Create a MySQL connection
connection = pymysql.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name,
    port=5432
)

# Create a cursor object
cursor = connection.cursor()

# Read data from the Excel file
workbook = load_workbook(excel_file_path, read_only=True)
sheet = workbook[sheet_name]

# Extract and insert data into MySQL table
table_name = 'dashboard_sdomaster'
for row in sheet.iter_rows(min_row=2, values_only=True):  # Assuming data starts from row 2
    # Assuming your table structure is (id, sdo_name, sdo_email, created_by, updated_by, created_date, updated_date, status)
    sdo_name = row[1] #row index need to insert
    sdo_email = row[2] if len(row) > 2 and row[2] is not None else 'NA'
    # created_by =1
    # updated_by =1
    # status='1'

    # Check if sdo_name is None or empty
    if sdo_name is None or sdo_name == '':
        print(f"Skipping row due to missing or empty 'sdo_name'.")
        continue

    # Construct the SQL INSERT statement with placeholders
    sql = f"INSERT INTO {table_name} (sdo_name, sdo_email) VALUES (%s, %s)"
    print(sql, '>>>>>>>>>>>>')

    # Execute the SQL statement with parameterized values
    cursor.execute(sql, (sdo_name, sdo_email))

# Commit the changes and close the connections
connection.commit()
cursor.close()
connection.close()

print(f"Data from sheet '{sheet_name}' successfully loaded into MySQL table '{table_name}'.")
import datetime

import pandas as pd
import MySQLdb

# Function to insert data into MySQL table
# def insert_into_mysql(data_frame, table_name, connection):
#     cursor = connection.cursor()
#
#     # Create the table if it doesn't exist
#     #
#
#     # Insert data into the table
#     data_frame = data_frame.where(pd.notna(data_frame), None)
#
#     print(data_frame,'>>>>>>>>>>>>>>>.')
#
#     for index, row in data_frame.iterrows():
#         region = row[0]  # row index need to insert
#         customer_name = row[1]
#         customer_id = row[2]
#         project_id = row[3]
#         opp_no = row[4]
#         success_service = row[5]
#         csm = row[6]
#         psm = row[7]
#         sdm = row[8]
#         industry = row[9]
#         success_elements = row[10]
#         description = row[11]
#         # date_created = datetime.date
#         cursor.execute(f"INSERT INTO {table_name} (region, customer_name, customer_id, project_id, opp_no, success_service, csm, psm, sdm, industry, success_elements, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
#                        (region, customer_name, customer_id, project_id, opp_no, success_service, csm, psm, sdm,
#                         industry, success_elements, description))
#         # Add more columns as needed
#
#     # Commit the changes
#     connection.commit()
#
# # Connect to MySQL database (replace with your database credentials)
# db_connection = MySQLdb.connect(host='localhost', user='root', password='test', database='ifsreporting_local')
#
# # Load Excel file into a Pandas DataFrame
# excel_file_path = '/home/rafique/Desktop/success_tool/apps/utility/data_mapping_1.xlsx'
# df = pd.read_excel(excel_file_path)
#
# # Specify the table name in the database
# table_name = 'dashboard_customerproject'
#
# # Call the function to insert data into the MySQL table
# insert_into_mysql(df, table_name, db_connection)
#
# # Close the database connection
# db_connection.close()



# import pandas as pd
# import MySQLdb
#
# def insert_into_mysql(data_frame, table_name, connection):
#     cursor = connection.cursor()
#
#     # Create the table if it doesn't exist
#     # ...
#
#     # Insert data into the table
#     data_frame = data_frame.where(pd.notna(data_frame), None)
#     print(data_frame,'>>>>>>>>>>>')
#
#     for index, row in data_frame.iterrows():
#         # print(index,'>>>>>>>>>>>',row)
#         # region = row[0]  # row index need to insert
#         # customer_name = row[1]
#         # customer_id = row[1]
#         # project_id = row[3]
#         # opp_no = row[4]
#         # success_service = row[5]
#         # csm = row[6]
#         # psm = row[7]
#         # sdm = row[8]
#         # industry = row[9]
#         # success_elements = row[10]
#         # description = row[11]
#         # cursor.execute(f"INSERT INTO {table_name} (region, customer_name, customer_id, project_id, opp_no, success_service, csm, psm, sdm, industry, success_elements, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
#         #                (region, customer_name, customer_id, project_id, opp_no, success_service, csm, psm, sdm,
#         #                 industry, success_elements, description))
#         # Extract data dynamically from every column in the row
#         column_values = [row[col] for col in data_frame.columns]
#
#         # Generate placeholders for the SQL query
#         placeholders = ', '.join(['%s'] * len(column_values))
#
#         # Generate column names for the SQL query
#         column_names = ', '.join(data_frame.columns)
#
#         # Execute the SQL query
#         cursor.execute(f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})", column_values)
#
#         # Add more columns as needed
#
#     # Commit the changes
#     connection.commit()
#
# # Connect to MySQL database (replace with your database credentials)
# db_connection = MySQLdb.connect(host='localhost', user='root', password='test', database='ifsreporting_local')
#
# # Load Excel file into a Pandas DataFrame for each sheet
# excel_file_path = '/home/rafique/Desktop/success_tool/apps/utility/data_mapping_1.xlsx'
# excel_sheets = pd.read_excel(excel_file_path, sheet_name=None)
#
# # Specify the table name in the database
# table_name = 'dashboard_customerproject'
#
# # Loop through each sheet and insert data into the MySQL table
# for sheet_name, df in excel_sheets.items():
#     if sheet_name == 'customer_project':
#         insert_into_mysql(df, table_name, db_connection)
#
# # Close the database connection
# db_connection.close()
