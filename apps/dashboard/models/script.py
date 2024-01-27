import openpyxl
import datetime
from django.contrib.auth.models import User
from apps.dashboard.models.masters import (
    StatusMaster,
    SdoMaster,
    MenuCardMaster,
    MenuSdoMapping,
    CustomerMaster,
    RegionMaster,
    ProjectMaster,
    SuccessServiceMaster,
    PSMMaster,
    CSMMaster,
    SDMMaster,
    IndustryMaster,
    SuccessElementsMaster,
    CustomerMapping,
)

def insert_from_excel(filename):
    try:
        wb = openpyxl.load_workbook(filename)
        ws = wb['customer_project']

        # Mapping of column names to their corresponding master models and their respective field names
        column_mapping = {
            'Region': (RegionMaster, 'region_name'),
            'Customer': (CustomerMaster, 'customer_name'),
            'Success Service': (SuccessServiceMaster, 'success_service_name'),
            'CSM': (CSMMaster, 'csm_name'),
            'PSM': (PSMMaster, 'psm_name'),
            'SDM': (SDMMaster, 'sdm_name'),
        }

        for row in ws.iter_rows(min_row=2, values_only=True):
            # Replace None values with empty strings
            row = ['' if value is None else value for value in row]

            # Fetch related master objects based on the values from the current row
            master_objects = {}
            for col_name, col_value in zip(ws[1], row):
                col_name = col_name.value
                if col_name in column_mapping and col_value != '':
                    model, field_name = column_mapping[col_name]
                    if model is not None:
                        try:
                            master_objects[col_name] = model.objects.get(**{field_name: col_value})
                        except model.DoesNotExist:
                            print(f"Master data not found for {col_name}: {col_value}. Skipping this column.")
                            break
                    else:
                        master_objects[col_name] = col_value

            else:
                # Create CustomerMapping instance if all master data is available
                customer_mapping_instance = CustomerMapping.objects.create(
                    region=master_objects.get('Region'),
                    customer=master_objects.get('Customer'),
                    success_service=master_objects.get('Success Service'),
                    csm=master_objects.get('CSM'),
                    psm=master_objects.get('PSM'),
                    sdm=master_objects.get('SDM'),
                    opp_no=row[4],
                    description=row[10],  # Assuming description is in the 11th column
                    created_by=User.objects.first(),  # Replace with appropriate user
                    created_date=datetime.datetime.now(),
                    updated_by=User.objects.first(),  # Replace with appropriate user
                    updated_date=datetime.datetime.now(),
                    status=StatusMaster.objects.first(),  # Replace with appropriate status
                )

        return True

    except FileNotFoundError:
        print(f"File not found: {filename}")
        return False
    except openpyxl.utils.exceptions.InvalidFileException:
        print(f"Invalid Excel file: {filename}")
        return False
    except Exception as e:
        print(f"An error occurred while reading the Excel file: {e}")
        return False

# Call function with Excel filename
insert_from_excel('E:\\IFS_BACKEND\\success_tool_backend_local\\report_creaton\\apps\\dashboard\\models\\data_mapping_1.xlsx')
