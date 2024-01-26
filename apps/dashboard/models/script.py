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
            'Customer': (CustomerMaster, 'customer_name'),
            'Region': (RegionMaster, 'region_name'),
            'Customer Id': (CustomerMaster, 'customer_id'),
            'Project Id': (ProjectMaster, 'project_name'),
            'Opp No.': None,  # No matching master model found
            'Success Service': (SuccessServiceMaster, 'success_service_name'),
            'CSM': (CSMMaster, 'csm_name'),
            'PSM': (PSMMaster, 'psm_name'),
            'SDM': (SDMMaster, 'sdm_name'),
            'Industry': (IndustryMaster, 'industry_type_name'),
            'Success Elements': (SuccessElementsMaster, 'success_element_name'),
            'Description': None,  # No matching master model found
        }

        for row in ws.iter_rows(min_row=2, values_only=True):
            # Replace blank values with "NA"
            row = ['NA' if value is None else value for value in row]

            # Fetch related master objects based on the values from the current row
            master_objects = {}
            for col_name, col_value in zip(ws[1], row):
                col_name = col_name.value
                if col_name in column_mapping and col_value != 'NA':
                    model, field_name = column_mapping[col_name]
                    if model is not None:
                        # Query master objects using the specified field name
                        try:
                            master_objects[col_name] = model.objects.filter(**{field_name: col_value}).first()
                        except model.DoesNotExist:
                            print(f"Master data not found for {col_name}: {col_value}. Skipping this column.")
                            break
                    else:
                        # No matching master model found, use the column value directly
                        master_objects[col_name] = col_value

            else:
                # Create CustomerMapping instance if all master data is available
                customer_mapping_instance = CustomerMapping.objects.create(
                    customer=master_objects['Customer'],
                    region=master_objects['Region'],
                    project=master_objects['Project Id'],  # Use 'Project Id' column
                    success_service=master_objects['Success Service'],
                    csm=master_objects.get('CSM'),
                    psm=master_objects.get('PSM'),
                    sdm=master_objects.get('SDM'),
                    industry=master_objects['Industry'],
                    description=master_objects['Description'],  # Use 'Description' column
                    created_by=User.objects.first(),  # Replace with appropriate user
                    created_date=datetime.datetime.now(),
                    updated_by=User.objects.first(),  # Replace with appropriate user
                    updated_date=datetime.datetime.now(),
                    status=StatusMaster.objects.first(),  # Replace with appropriate status
                )

                # Add success elements if available
                if 'Success Elements' in master_objects:
                    customer_mapping_instance.success_elements.add(master_objects['Success Elements'])

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
