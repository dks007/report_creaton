from datetime import datetime
from apps.dashboard.models import SuccessReport
from apps.dashboard.models.masters import CustomerMapping, MenuSdoMapping, MenuCardMaster, ReportStatusMaster
from django.core.exceptions import ObjectDoesNotExist
import re
# common functions used by various apps
def convert_date(date_str):
    if date_str is None:
        return None
        # Define input and output formats
    input_formats = ["%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%dT%H:%M:%S.%f%z"]
    output_format = "%d %b %Y"
    # If the input is already a datetime object, use it directly
    if isinstance(date_str, datetime):
        parsed_date = date_str
    else:
        # Try parsing the input date using each format
        for format_str in input_formats:
            try:
                parsed_date = datetime.strptime(date_str, format_str)
                # If parsing is successful, break out of the loop
                break
            except ValueError:
                pass
        else:
            # If none of the formats work, raise an error
            raise ValueError("Invalid date format")

    # Format the date in the desired output format
    formatted_date = parsed_date.strftime(output_format)

    return formatted_date

def get_productCapability(input_data):
    """
    Extracts product capability, product name, product version, and frequency from JSON data.

    Args:
    input_data (dict): Input JSON data.

    Returns:
    tuple: A tuple containing capability, product name, product version, and frequency.
    """
    CAPABILITY_KEY = "primary industry:"
    PRODUCT_KEY = "product:"
    FREQUENCY_KEY = "frequency:"

    capability = None
    product_name = None
    product_version = None
    frequency = None

    content_items = input_data.get("content", [])
    for content_item in content_items:
        if content_item.get("type") == "paragraph":
            text_items = [item.get("text", "") for item in content_item.get("content", [])]
            for line in text_items:
                line = line.strip()
                if line.lower().startswith(CAPABILITY_KEY):
                    capability = line.split(":")[1].strip()
                    capability = None if capability.lower() =="undefined" else capability
                elif line.lower().startswith(PRODUCT_KEY):
                    product_line = line.split(":")[1].strip()
                    product_parts = product_line.split()
                    if any(part.replace('.', '', 1).isdigit() for part in product_parts):
                        product_name_parts = product_parts[:-1] if "IFS Cloud" in product_line else product_parts
                        product_name = " ".join(product_name_parts)
                        product_version = next((part for part in product_parts if part.replace('.', '', 1).isdigit()), "NA")
                    else:
                        product_name = product_line
                        product_version = "NA"
                elif line.lower().startswith(FREQUENCY_KEY):
                    frequency = line.split(":")[1].strip()

    return capability, product_name, product_version, frequency


# Function to extract product and capability
def get_productCapability_old(json_data):
    #json_data = json.loads(json_data)
    capability = None
    product_version = None
    product_name = None
    frequency = None

    for content_item in json_data.get("content", []):
        if content_item.get("type") == "paragraph":
            
            text_items = [item.get("text", "") for item in content_item.get("content", [])]
            for i in range(len(text_items)):
                line = text_items[i].strip()

                if line.lower().startswith("primary industry:"):
                    capability = line.split(":")[1].strip()
                    capability = None if capability.value.lower() =="undefined" else capability.value

                if line.lower().startswith("product:"):
                    product_line = line.split(":")[1].strip()
                    if i + 1 < len(text_items) and not text_items[i + 1].strip().lower().startswith("current software version:"):
                        product_parts = product_line.split()
                        #product_name = product_line if not any(part.replace('.', '', 1).isdigit() for part in product_parts) else " ".join(product_parts[:-1])
                        product_name = product_line
                        product_version = next((part for part in product_parts if part.replace('.', '', 1).isdigit()), "NA")
                    else:
                        product_name = product_line
                        product_version = "NA"

                if line.lower().startswith("frequency:"):
                    frequency = line.split(":")[1].strip()
    
    return capability, product_name, product_version, frequency    
# function to get subtasks list
def extract_subtasks_data(subtasks):
    # Check if "subtasks" is not empty
    if subtasks:
        # Extracting key and summary of subtasks
        subtasks_data = []
        for subtask in subtasks:
            subtask_data = {
                "key": subtask.get("key", ""),
                "summary": subtask.get("fields", {}).get("summary", "")
            }
            subtasks_data.append(subtask_data)
        return subtasks_data
    else:
        return []

# getting menu card and partner by given string
def find_menuid_in_string(match_str, menuList):
    if match_str:
        match_str = match_str.strip()  # Trim leading and trailing whitespace
        match = re.search(r'(QSM|SAA|EMA|TAA)(0*\d+)P?', match_str)
        if match:
            menu_prefix = match.group(1)
            menu_number = match.group(2)
            menu_id_with_zeros = menu_prefix + menu_number
            menu_id_without_zeros = menu_prefix + str(int(menu_number))  # Convert menu number to integer to remove leading zeros
            
            if menu_id_with_zeros in menuList:
                return menu_id_with_zeros, match.group().endswith('P')
            elif menu_id_without_zeros in menuList:
                return menu_id_without_zeros, match.group().endswith('P')
            else:
                return None, False
        else:
            return None, False
    return None, False

# get report data to write document
def getSuccessReportData(issueKey):
    try:
        issue_data_dict = {}
        
        # Attempt to retrieve report data
        report_data = SuccessReport.objects.filter(jira_key=issueKey).first()
        
        # If report_data is None, no record with the provided issueKey was found
        if report_data is None:
            return None
        
        # Extract data from report_data and populate issue_data_dict
        issue_data_dict['sdo_name'] = report_data.sdo.sdo_name.strip()
        issue_data_dict['csm_name'] = report_data.csm.csm_name.strip()
        issue_data_dict['sdm_name'] = report_data.sdm.sdm_name.strip()
        issue_data_dict['snow_case_no'] = report_data.snow_case_no.strip()
        issue_data_dict['menu_card'] = report_data.menu_card.menu_card.strip()
        issue_data_dict['menu_description'] = report_data.menu_card.menu_description.strip()
        issue_data_dict['expert_name'] = report_data.expert.expert_name.strip()
        issue_data_dict['product_name'] = report_data.product.product_name.strip()
        issue_data_dict['capability_name'] = report_data.capability.capability_name.strip()
        issue_data_dict['sub_capability_name'] = report_data.sub_capability.sub_capability_name.strip()
        issue_data_dict['customer_name'] = report_data.customer.customer_name.strip()
        issue_data_dict['customer_contact'] = report_data.customer_contact.customer_contact.strip()
        issue_data_dict['logo'] = report_data.logo.logo_image

        return issue_data_dict
    
    except ObjectDoesNotExist:
        # Handle the case where any of the related objects do not exist
        return None
        

# function to get sdm, csm, sdo , report status and error message 
def getAdditionDataBKey(issue_data_dict):
    # Additional processing and enriching the issue_data_dict
        report_data = SuccessReport.objects.filter(jira_key=issue_data_dict.get('issue_key')).first()
        menu_card_data = MenuCardMaster.objects.filter(menu_card=issue_data_dict.get('menu_card')).first()
        sdo_map = MenuSdoMapping.objects.filter(menu_card__menu_card=issue_data_dict.get('menu_card')).first()
        customer_map = CustomerMapping.objects.filter(customer__customer_id=issue_data_dict.get('customer_id')).first()

        # check if records exists in success report table
        if report_data:
            issue_data_dict['report_status'] = str(report_data.report_status.id)
            issue_data_dict['report_error'] = report_data.error_msg

            if report_data.sdo:
                issue_data_dict['sdo_name'] = report_data.sdo.sdo_name
            else:
                issue_data_dict['sdo_name'] = ''

            if report_data.csm:
                issue_data_dict['csm_name'] = report_data.csm.csm_name
            else:
                issue_data_dict['csm_name'] = ''

            if report_data.sdm:
                issue_data_dict['sdm_name'] = report_data.sdm.sdm_name
            else:
                issue_data_dict['sdm_name'] = ''

            issue_data_dict['menu_description'] = report_data.menu_card.menu_description
            issue_data_dict['menu_card'] = report_data.menu_card.menu_card
            issue_data_dict['customer_name'] = report_data.customer.customer_name
            issue_data_dict['snow_case_no'] = report_data.snow_case_no
            issue_data_dict['customer_contact'] = report_data.customer_contact.customer_contact
            issue_data_dict['product'] = report_data.product.product_name
            issue_data_dict['capability'] = report_data.capability.capability_name
            issue_data_dict['sub_capability'] = report_data.sub_capability.sub_capability_name
            issue_data_dict['logo_file_name'] = report_data.logo.logo_file_name
            issue_data_dict['logo_url'] = report_data.logo.logo_url
        else:
            if sdo_map and sdo_map.sdo:
                issue_data_dict['sdo_name'] = sdo_map.sdo.sdo_name if sdo_map.sdo else ''
            else:
                issue_data_dict['sdo_name']=''

            if menu_card_data is not None:
                issue_data_dict['menu_card'] = menu_card_data.menu_card if menu_card_data.menu_card else ''
                issue_data_dict['menu_description'] = menu_card_data.menu_description if menu_card_data.menu_description else ''

            if customer_map:
                issue_data_dict['csm_name'] = customer_map.csm.csm_name if customer_map.csm else ''
                issue_data_dict['sdm_name'] = customer_map.sdm.sdm_name if customer_map.sdm else ''
            else:
                issue_data_dict['csm_name']=''
                issue_data_dict['sdm_name']=''

            issue_data_dict['report_status'] = '1'
            issue_data_dict['report_error'] = ''
            issue_data_dict['sub_capability'] =''
        return issue_data_dict

# get issue description text
def get_description_content(obj):
    if "content" in obj:
        content = obj["content"]
        text_content = ""
        for item in content:
            if item["type"] == "paragraph":
                paragraph_content = item["content"]
                for element in paragraph_content:
                    if element["type"] == "text":
                        text_content += element["text"]
                    elif element["type"] == "hardBreak":
                        text_content += "\n"
                text_content += "\n"  # Add newline after each paragraph
        return text_content.strip()  # Remove leading/trailing whitespace

# update report status
def update_report_status(pk, report_status_id, download_link=None):
    try:
        success_report = SuccessReport.objects.get(pk=pk)
        if download_link:
            success_report.download_link = download_link
        report_status_instance = ReportStatusMaster.objects.get(pk=report_status_id)
        success_report.report_status = report_status_instance
        success_report.save()
        return True, f"SuccessReport with pk {pk} updated successfully."
    except SuccessReport.DoesNotExist:
        return False, f"SuccessReport with pk {pk} does not exist."
    except ReportStatusMaster.DoesNotExist:
        return False, f"ReportStatusMaster with id {report_status_id} does not exist."
    except Exception as e:
        return False, f"An error occurred: {str(e)}"