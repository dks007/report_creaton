import requests
import json
from requests.auth import HTTPBasicAuth
import os
import django
from apps.dashboard.models import SuccessReport
from apps.dashboard.models.masters import CustomerMapping, MenuSdoMapping, MenuCardMaster
from datetime import datetime
from apps.utility import utils
from .jqlconfig import headers, auth
from .jqlpayload_details import construct_payload

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "success_tool.settings")
django.setup()


def create_report(request, id):
    """
    Fetches issue data from Jira API and populates a Django model with the extracted data.

    Args:
        issue_key (str): jira issue key

    Returns:
        tuple: response data provide individual records of issue key.
    """
    # Construct payload using jqlpayload.py
    payload = construct_payload(request, id)
    # Getting request
    issue_key = request.GET.get('issue_key')
    emailId = "dilip.kumar.shrivastwa@ifs.com"

    # url = os.getenv('JIRA_URL')
    # Send request to Jira API
    # response = requests.request(
    #     "POST",
    #     url,
    #     headers=headers,
    #     auth=auth,
    #     data=json.dumps(payload),
    #     verify=False
    # )

    json_file_path = "/home/rafique/Desktop/reporting/apps/utility/singledata.json"
    # Open the file in read mode
    with open(json_file_path, "r", encoding='utf-8') as json_file:
        data = json.load(json_file)

        # if response.status_code == 200:
    if True:
        # issues_data = json.loads(response.text)
        issues_data = data
        total_records = issues_data['total']
        # call menu card from MenucardMaster database
        menuList = list(MenuCardMaster.objects.values_list('menu_card', flat=True))
        issue = issues_data['issues'][0]  # Extracting the single issue
        menu_card = None
        partner = False
        menu_description = ''
        customer_id = ''
        activit_project_id = ''
        capability = ''
        product = ''
        product_version = ''
        frequency = ''
        changelog = issue.get("changelog", {}).get("histories", [])
        changelog_assignee_created = None

        # get subtask list
        subtasks = issue["fields"].get('subtasks', [])
        subtasks_list = utils.extract_subtasks_data(subtasks)
        description = issue["fields"].get('description', "")

        if description:
            capability, product, product_version, frequency = utils.get_productCapability(description)

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
        created = utils.convert_date(created)
        parent_id = issue["fields"]["parent"].get("id", "") if "parent" in issue["fields"] else None
        parent_key = issue["fields"]["parent"].get("key", "") if "parent" in issue["fields"] else None
        parent_summary = issue["fields"]["parent"]["fields"].get('summary', "") if "parent" in issue[
            "fields"] else None

        activity_short_name = issue["fields"].get("customfield_16036", "")
        if activity_short_name and '.' in activity_short_name:
            activity_split_string = activity_short_name.split('.')
            # getting activity project id
            activit_project_id = activity_split_string[0]
            # getting activit menuid string
            activit_menu_string = activity_split_string[2]
            # call function to get menu id and partner
            menu_card, partner = utils.find_menuid_in_string(activit_menu_string, menuList)
            # print("menu_card1111->",issue_key,menu_card)
        if menu_card is None:
            menu_card, partner = utils.find_menuid_in_string(issue_summary, menuList)
            # print("menu_card2222->",issue_key,menu_card)
        if menu_card is None:
            menu_card, partner = utils.find_menuid_in_string(parent_summary, menuList)
            # print("menu_card333->",issue_key,menu_card)
        if menu_card is None:
            menu_card = None
            partner = False

        changelog_assignee_created = utils.convert_date(changelog_assignee_created)
        creator_email = issue["fields"]["creator"].get("emailAddress", "") if "creator" in issue["fields"] else None
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
        snow_case_no = issue["fields"].get("customfield_16266", "")
        subtask = issue["fields"]["issuetype"].get("subtask", "")

        assignee_name = issue["fields"]["assignee"].get("displayName", "") if "assignee" in issue[
            "fields"] else None
        assignee_email = issue["fields"]["assignee"].get("emailAddress", "") if "assignee" in issue[
            "fields"] else None
        assignee_id = issue["fields"]["assignee"].get("accountId", "") if "assignee" in issue[
            "fields"] else None

        issue_status = issue["fields"]["status"].get("name", "")

        # Create an Issue instance
        issue_data_dict = {
            "issue_key": issue_key,
            "menu_card": menu_card,
            "capability": capability,
            "product": product,
            "project_name": project_name,  # customer name/proect name
            "snow_case_no": snow_case_no,
            "creator_email": creator_email,
            "assignee_name": assignee_name,  # expert name
            "creator_name": creator_name  # creator name
        }

        # Additional processing and enriching the issue_data_dict
        report_data = SuccessReport.objects.filter(jira_key=issue_data_dict.get('issue_key')).first()

        if report_data:
            issue_data_dict['report_status'] = str(report_data.report_status.id)
            # issue_data_dict['report_error'] = report_data.error_msg
        else:
            issue_data_dict['report_status'] = '0'

        return [issue_data_dict]  # Returning a list with a single record and total count
