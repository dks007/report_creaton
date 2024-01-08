# reporting/tasks.py
from requests.auth import HTTPBasicAuth
import requests
import json
import csv, re
import time
from datetime import datetime


# Function to extract product and capability
def get_productCapability(json_data):
    # json_data = json.loads(json_data)
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

                if line.lower().startswith("product:"):
                    product_line = line.split(":")[1].strip()
                    if i + 1 < len(text_items) and not text_items[i + 1].strip().lower().startswith(
                            "current software version:"):
                        product_parts = product_line.split()
                        # product_name = product_line if not any(part.replace('.', '', 1).isdigit() for part in product_parts) else " ".join(product_parts[:-1])
                        product_name = product_line
                        product_version = next((part for part in product_parts if part.replace('.', '', 1).isdigit()),
                                               "NA")
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

    # Function to find the menu id and partner from activity short menu


def find_menuid_in_string(match_str):
    if match_str is None:
        return None, False
    match_str = match_str.strip()
    menu_list = ['QSM1', 'QSM2', 'QSM3', 'QSM4', 'QSM5', 'QSM6', 'QSM7', 'QSM8', 'QSM9', 'QSM10', 'QSM11', 'QSM12',
                 'SAA1', 'SAA2', 'SAA3', 'SAA4', 'SAA5', 'SAA6', 'SAA7', 'SAA8', 'SAA9', 'SAA10', 'SAA11', 'SAA12',
                 'SAA13',
                 'SAA14', 'SAA15', 'TAA1', 'TAA2', 'TAA3', 'TAA4', 'TAA5', 'TAA6', 'TAA7', 'TAA8', 'TAA9', 'EMA1',
                 'EMA2', 'EMA3',
                 'EMA4', 'EMA5', 'EMA6', 'EMA7', 'EMA8', 'EMA9', 'EMA10', 'EMA11', 'EMA12', 'EMA13', 'EMA14']

    normalized_match_str = re.sub(r'(\D)0+(\d)', r'\1\2', match_str)

    matching_values = [menu_item for menu_item in menu_list if
                       re.sub(r'(\D)0+(\d)', r'\1\2', menu_item) in normalized_match_str]

    if matching_values:
        menu_id = max(matching_values, key=len)
        index_of_match = normalized_match_str.find(menu_id)
        p_is_after_match = (index_of_match + len(menu_id) < len(normalized_match_str)) and (
                    normalized_match_str[index_of_match + len(menu_id)] == 'P')
        return menu_id, p_is_after_match
    return None, False


MAX_DURATION_SECONDS = 60
start_time = time.time()
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}
url = "https://ifsdev.atlassian.net/rest/api/3/search"
auth = HTTPBasicAuth("dilip.kumar.shrivastwa@ifs.com",
                     "ATATT3xFfGF0p-FG8-lj6HsWs80g3AtzRePPZ4WDbZEq_ZlDJoEVV3zcusdMdiyGxn1do8ldFe4Tgy4OcC2gOc9yArvRSzZ24z13JqWPxKsJvvinVybUIwYdlnla8QErcuYl0XnMBvLc_Fn_sk2TntBf1Rj4DZ-hkL5FOr4xu5kDo9M2rna2vEQ=B3F4BE74")
# cutome fields names
# customfield_16032 => customer contact
# customfield_16015 => start date
# customfield_16036 => Activit Short name
# customfield_16262 => Customer email
# customfield_16263 => customer contact number
# customfield_16264 => custome region/location
# customfield_16265 => SNow Request Item No
# set the initial parameters
payload = {
    "expand": [
        "changelog"
    ],
    "jql": "issuetype in (Sub-task, Tasks) AND status in ('Awaiting Customer', 'In Process','In Review','Not Started') AND 'Service Category[Dropdown]' = 'Expert Services' AND assignee NOT in (EMPTY) order by created DESC",
    "fieldsByKeys": False,
    "fields": [
        "summary",
        "description",
        "project",
        "customfield_16032",
        "customfield_16015",
        "customfield_16036",
        "customfield_16262",
        "customfield_16263",
        "customfield_16264",
        "customfield_16265",
        "assignee",
        "issuetype",
        "status",
        "parent",
        "created",
        "creator",
        "subtasks",
        "comment"
    ],
    "maxResults": 100,
    "startAt": 0
}

csv_file_path = "all_issue_new_3.csv"

# Write the header row only once
with open(csv_file_path, mode='a', encoding='utf-8', newline='') as csv_file:
    fieldnames = [
        "issue_summary",
        "menu_card",
        "issue_id",
        "issue_key",
        "parent_key",
        "parent_summary",
        "activity_short_name",
        "subtasks_list",
        "partner",
        "subtask",
        "capability",
        "product",
        "product_version",
        "frequency",
        "activit_project_id",
        "project_id",
        "project_key",
        "customer_id",
        "project_name",
        "customer_email",
        "customer_contact_no",
        "customer_contact",
        "customer_location",
        "snow_request_no",
        "created",
        "changelog_assignee_created",
        "creator_email",
        "parent_id",
        "assignee_email",
        "assignee_name",
        "creator_name",
        "assignee_id",
        "issue_status"
    ]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

while True:
    response = requests.request(
        "POST",
        url,
        headers=headers,
        auth=auth,
        data=json.dumps(payload),
        verify=False
    )

    # check if the request response was successful
    if response.status_code == 200:
        issues_data = json.loads(response.text)

        # Write the extracted fields for each issue to the CSV file
        with open(csv_file_path, mode='a', encoding='utf-8', newline='') as csv_file:
            fieldnames = [
                "issue_summary",
                "menu_card",
                "issue_id",
                "issue_key",
                "parent_key",
                "parent_summary",
                "activity_short_name",
                "subtasks_list",
                "partner",
                "subtask",
                "capability",
                "product_name",
                "product_version",
                "frequency",
                "activit_project_id",
                "project_id",
                "project_key",
                "customer_id",
                "project_name",
                "customer_email",
                "customer_contact_no",
                "customer_contact",
                "customer_location",
                "snow_request_no",
                "created",
                "changelog_assignee_created",
                "creator_email",
                "parent_id",
                "assignee_email",
                "assignee_name",
                "creator_name",
                "assignee_id",
                "issue_status"
            ]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            customer_id = ''
            capability = ''
            product_name = ''
            product_version = ''
            frequency = ''
            # Insert data into Django model
            for issue in issues_data['issues']:
                menu_card = ''
                partner = ''
                customer_id = ''
                # subtask_list = []
                activit_project_id = ''
                changelog = issue.get("changelog", {}).get("histories", [])
                changelog_assignee_created = None
                # get subtask list
                subtasks = issue["fields"].get('subtasks', [])
                subtasks_list = extract_subtasks_data(subtasks)
                description = issue["fields"].get('description', "")
                # print("description-->",description)

                if description:
                    capability, product_name, product_version, frequency = get_productCapability(description)

                # Extract assignee and created date from changelog
                for history in changelog:
                    for item in history.get("items", []):
                        if item.get("field") == "assignee":
                            created_date_str = history.get("created", "")
                            created_date = datetime.strptime(created_date_str, "%Y-%m-%dT%H:%M:%S.%f%z")
                            if changelog_assignee_created is None or created_date < changelog_assignee_created:
                                changelog_assignee_created = created_date

                issue_summary = issue["fields"].get('summary', "")
                issue_id = issue.get("id", "")
                issue_key = issue.get("key", "")
                created = issue["fields"].get('created', "")
                parent_id = issue["fields"]["parent"].get("id", "") if "parent" in issue["fields"] else None
                parent_key = issue["fields"]["parent"].get("key", "") if "parent" in issue["fields"] else None
                parent_summary = issue["fields"]["parent"]["fields"].get('summary', "") if "parent" in issue[
                    "fields"] else None
                activity_short_name = issue["fields"].get("customfield_16036", "")
                if activity_short_name and '.' in activity_short_name:
                    activity_split_string = activity_short_name.split('.')
                    activit_project_id = activity_split_string[0]
                    activit_menu_string = activity_split_string[2]
                    menu_card, partner = find_menuid_in_string(activit_menu_string)
                # Check if menu_card is still None after the first condition
                if menu_card is None or menu_card == '':
                    menu_card, partner = find_menuid_in_string(issue_summary)
                # Check if menu_card is still None after the second condition
                if menu_card is None or menu_card == '':
                    menu_card, partner = find_menuid_in_string(parent_summary)

                changelog_assignee_created = changelog_assignee_created
                creator_email = issue["fields"]["creator"].get("emailAddress", "") if "creator" in issue[
                    "fields"] else None
                creator_name = issue["fields"]["creator"].get("displayName", "") if "creator" in issue[
                    "fields"] else None
                menu_card = menu_card
                partner = partner
                activit_project_id = activit_project_id
                project_id = issue["fields"]["project"].get("id", "")
                project_name = issue["fields"]["project"].get("name", "")
                project_key = issue["fields"]["project"].get("key", "")
                # get customer id from project key
                customer_id = project_key[2:]
                customer_email = issue["fields"].get("customfield_16262", "")
                customer_contact_no = issue["fields"].get("customfield_16263", "")
                customer_location = issue["fields"]["customfield_16264"].get("value", "") if issue["fields"][
                    "customfield_16264"] else None
                customer_contact = issue["fields"].get("customfield_16032", "")
                snow_request_no = issue["fields"].get("customfield_16265", "")
                subtask = issue["fields"]["issuetype"].get("subtask", "")

                assignee_name = issue["fields"]["assignee"].get("displayName", "") if "assignee" in issue[
                    "fields"] else None
                assignee_email = issue["fields"]["assignee"].get("emailAddress", "") if "assignee" in issue[
                    "fields"] else None
                assignee_id = issue["fields"]["assignee"].get("accountId", "") if "assignee" in issue[
                    "fields"] else None

                issue_status = issue["fields"]["status"].get("name", "")

                # Create an Issue instance
                issue_fields = {
                    "issue_summary": issue_summary,
                    "menu_card": menu_card,
                    "issue_id": issue_id,
                    "issue_key": issue_key,
                    "parent_key": parent_key,
                    "parent_summary": parent_summary,
                    "activity_short_name": activity_short_name,
                    "subtasks_list": subtasks_list,
                    "partner": partner,
                    "subtask": subtask,
                    "capability": capability,
                    "product_name": product_name,
                    "product_version": product_version,
                    "frequency": frequency,
                    "activit_project_id": activit_project_id,
                    "project_id": project_id,
                    "project_key": project_key,
                    "customer_id": customer_id,
                    "project_name": project_name,
                    "customer_email": customer_email,
                    "customer_contact_no": customer_contact_no,
                    "customer_contact": customer_contact,
                    "customer_location": customer_location,
                    "snow_request_no": snow_request_no,
                    "created": created,
                    "changelog_assignee_created": changelog_assignee_created.isoformat() if changelog_assignee_created else None,
                    "creator_email": creator_email,
                    "parent_id": parent_id,
                    "assignee_email": assignee_email,
                    "assignee_name": assignee_name,
                    "creator_name": creator_name,
                    "assignee_id": assignee_id,
                    "issue_status": issue_status
                }

                # Save the instance to the csv
                writer.writerow(issue_fields)

            # check if there are more issues to retrieve
            if time.time() - start_time > MAX_DURATION_SECONDS:
                print("time exceeds!")
                break
            if issues_data['startAt'] + issues_data['maxResults'] < issues_data['total']:
                # increment the startAt parameter for the next request
                payload['startAt'] += issues_data['maxResults']
                print(payload['startAt'])
            else:
                # all issues have been retrieved
                break

    else:
        # print an error if the request was not successful
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        # print(response.text)
        break

print("Data has been saved successfully!")
