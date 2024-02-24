# utils.py

import requests
from requests.auth import HTTPBasicAuth  # Use the appropriate authentication method
from django.conf import settings
from docxtpl import DocxTemplate, InlineImage
from utility.utils import getSuccessReportData

# creating Report file from template
def executeSchedulerJob(issueKey):

    #getData = getSuccessReportData(issueKey)
    print ("Inside the SchedulerJob Class executeSchedulerJob method")
    doc = DocxTemplate ("C:\\Users\\lokain\\Documents\\workarea\\Success-Pilot-Web-Project\\IFS_Success_Final_Report_Template.docx")
    #context = {'workplan_number' : '123' , 'person' : 'lokesh', 'location':'Bangalore'}
    context = {
        'Insert_MenuCard_Service_Heading_and_Number_Here' : 'Solution design best practices for IFS Software deployments - SAA2',
        'Insert_Customer_branding_here' : InlineImage (doc, 'C:\\Users\\lokain\\Documents\\workarea\\Success-Pilot-Web-Project\\acmeCorporation.png'),
        'customer_name' : 'ACME Corporation',
        'List_the_names_of_the_participants_from_IFS' : 'Lokesh Kannaiah',
        'List_the_names_of_the_participants_from_customer': 'Satpal, Dilip Kumar',
        'ServiceNow_ID' : 'CS009876534'
        }
    doc.render(context)

def create_folder_and_upload_to_sharepoint(success_report):
    base_url = settings.SHAREPOINT_BASE_URL
    site_url = settings.SHAREPOINT_SITE_URL
    username = settings.SHAREPOINT_USERNAME
    password = settings.SHAREPOINT_PASSWORD

    folder_name = success_report.jira_key
    file_name = success_report.logo.logo_file_name
    file_content = success_report.logo.logo.tobytes()

    # Step 1: Create Folder
    folder_endpoint = f"{base_url}/{site_url}/_api/Web/Folders"
    folder_payload = {
        "__metadata": {"type": "SP.Folder"},
        "ServerRelativeUrl": f"{site_url}/{folder_name}",
    }
    folder_headers = {
        "Accept": "application/json;odata=verbose",
        "Content-Type": "application/json;odata=verbose",
    }

    folder_response = requests.post(
        folder_endpoint,
        json=folder_payload,
        headers=folder_headers,
        auth=HTTPBasicAuth(username, password),
    )

    if folder_response.status_code != 201:
        raise Exception(f"Failed to create folder. Response: {folder_response.text}")

    # Step 2: Upload File
    folder_url = folder_response.json()["d"]["ServerRelativeUrl"]
    file_endpoint = f"{base_url}/{site_url}/{folder_url}/{file_name}"

    file_headers = {
        "Accept": "application/json;odata=verbose",
        "Content-Type": "application/octet-stream",
    }

    file_response = requests.put(
        file_endpoint,
        data=file_content,
        headers=file_headers,
        auth=HTTPBasicAuth(username, password),
    )

    if file_response.status_code != 200:
        raise Exception(f"Failed to upload file. Response: {file_response.text}")

    # Step 3: Get File Download Link
    download_link_endpoint = f"{base_url}/{site_url}/_api/Web/GetFileByServerRelativeUrl('{folder_url}/{file_name}')/$value"
    download_link_response = requests.get(
        download_link_endpoint,
        headers={"Accept": "application/json;odata=verbose"},
        auth=HTTPBasicAuth(username, password),
    )

    if download_link_response.status_code != 200:
        raise Exception(f"Failed to get download link. Response: {download_link_response.text}")

    return download_link_response.text
