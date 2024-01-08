from requests.auth import HTTPBasicAuth
import requests
import json
import csv
import time
from datetime import datetime
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "success_tool.settings")

import django
django.setup()

from apps.dashboard.models import MenuCardMaster


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


def format_date(input_date, input_format="%Y-%m-%dT%H:%M:%S.%f%z"):
    if input_date is None:
        return None
    if isinstance(input_date, datetime):
        # If the input is already a datetime object, just format it
        formatted_date = input_date.strftime("%-d %b %Y")
        return formatted_date

    try:
        # Parse the input date string
        parsed_date = datetime.strptime(input_date, input_format)

        # Truncate microseconds and format the date using f-string
        parsed_date = parsed_date.replace(microsecond=0)
        formatted_date = f"{parsed_date.day} {parsed_date.strftime('%b %Y')}"
        return formatted_date

    except ValueError as e:
        # Handle the case where the input date string is not in the expected format
        print(f"Error: {e}")
        return None

    # def getCustomerId(proectKey):


# Function to find the menu id and partner from activity short menu
def find_menuid_in_string(match_str):
    menuList = list(MenuCardMaster.objects.values_list('menu_card', flat=True))
    # need to fetch from database dashboard_menusdo
    menuList1 = ['QSM1', 'QSM2', 'QSM3', 'QSM4', 'QSM5', 'QSM6', 'QSM7', 'QSM8', 'QSM9', 'QSM10', 'QSM11', 'QSM12',
                'SAA1', 'SAA2', 'SAA3', 'SAA4', 'SAA5', 'SAA6', 'SAA7', 'SAA8', 'SAA9', 'SAA10', 'SAA11', 'SAA12',
                'SAA13',
                'SAA14', 'SAA15', 'TAA1', 'TAA2', 'TAA3', 'TAA4', 'TAA5', 'TAA6', 'TAA7', 'TAA8', 'EMA1', 'EMA2',
                'EMA3',
                'EMA4', 'EMA5', 'EMA6', 'EMA7', 'EMA8', 'EMA9', 'EMA10', 'EMA11', 'EMA12', 'EMA13', 'EMA14']
    matching_values = [menu_item for menu_item in menuList if menu_item in match_str]
    longest_matching_value = ''
    p_is_after_match = ''
    longest_matching_value = max(matching_values, key=len, default=None)

    if longest_matching_value is not None:
        index_of_match = match_str.find(longest_matching_value)
        p_is_after_match = (
                                   index_of_match + len(longest_matching_value) < len(match_str)) and (
                                   match_str[index_of_match + len(longest_matching_value)] == 'P')
        return longest_matching_value, p_is_after_match
    return None, False


def specific_data(iss_id):
    MAX_DURATION_SECONDS = 60

    # issueId = 1990817

    payload = {
        "expand": [
            "changelog"
        ],
        "jql": f"issuetype in (Sub-task, Tasks) AND status in ('Awaiting Customer', 'In Process','In Review','Not Started') AND 'Service Category[Dropdown]' = 'Expert Services' AND key in({iss_id}) AND assignee NOT in (EMPTY) order by created DESC",
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
            "subtask",
            "comment"
        ]
    }
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
    # Specify the start and end parameters

    response = requests.request(
        "POST",
        url,
        headers=headers,
        data=json.dumps(payload),
        auth=auth,
        verify=False
    )

    # check if the request response was successful
    if response.status_code == 200:
        issues_data = json.loads(response.text)
        issue = issues_data['issues'][0]
        menu_card = ''
        menu_description = ''
        partner = ''
        customer_id = ''
        activit_project_id = ''
        changelog = issue.get("changelog", {}).get("histories", [])
        changelog_assignee_created = None

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
        created = convert_date(created)
        activity_short_name = issue["fields"].get("customfield_16036", "")
        if activity_short_name and '.' in activity_short_name:
            activity_split_string = activity_short_name.split('.')
            # getting activity project id
            activit_project_id = activity_split_string[0]
            # getting activit menuid string
            activit_menu_string = activity_split_string[2]
            # call function to get menu id and partner
            menu_card, partner = find_menuid_in_string(activit_menu_string)
        else:
            menu_card, partner = find_menuid_in_string(issue_summary)

        changelog_assignee_created = convert_date(changelog_assignee_created)
        creator_email = issue["fields"]["creator"].get("emailAddress", "") if "creator" in issue["fields"] else None

        menu_card = menu_card
        # if menu_card :
        # menu_description = getmenudescription()

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
        parent_id = issue["fields"]["parent"].get("id", "") if "parent" in issue["fields"] else None
        parent_key = issue["fields"]["parent"].get("key", "") if "parent" in issue["fields"] else None
        parent_summary = issue["fields"]["parent"]["fields"].get('summary', "") if "parent" in issue[
            "fields"] else None

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
            "issue_key": issue_key,
            "issue_summary": issue_summary,
            "menu_card": menu_card,
            "menu_description": menu_description,
            "activity_short_name": activity_short_name,
            "partner": partner,
            # "activit_project_id": activit_project_id,
            "project_id": project_id,
            "project_key": project_key,
            "customer_id": customer_id,
            "project_name": project_name,
            # "customer_email": customer_email,
            "customer_contact_no": customer_contact_no,
            "customer_contact": customer_contact,
            "customer_location": customer_location,
            # "snow_request_no": snow_request_no,
            # "issue_id": issue_id,
            "created": created,
            "changelog_assignee_created": changelog_assignee_created if changelog_assignee_created else None,
            # "creator_email": creator_email,
            # "parent_id": parent_id,
            # "parent_key": parent_key,
            "parent_summary": parent_summary,
            "subtask": subtask,
            # "assignee_email": assignee_email,
            "assignee_name": assignee_name,
            # "assignee_id": assignee_id,
            "issue_status": issue_status
        }

        # Save the instance to the csv
        # data_list.append(issue_fields)

        # Convert the list of dictionaries to a JSON string
        # json_data = json.dumps(issue_fields, indent=2)
        # Print or save the JSON data as needed
        print(issue_fields)
        print("Data has been fetched successfully!")
        return issue_fields



    else:
        # print an error if the request was not successful
        print(f"Failed to retrieve data. Status code: {response.status_code}")