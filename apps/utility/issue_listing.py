import requests
import json
import os
import django
from apps.dashboard.models import SuccessReport
from apps.dashboard.models.masters import CustomerMapping, MenuSdoMapping, MenuCardMaster
from datetime import datetime
from apps.utility.utils import getSuccessReportData, getAdditionDataBKey, convert_date, extract_subtasks_data , get_productCapability, find_menuid_in_string
from .jqlconfig import headers, auth
from .jqlpayload import construct_payload
from .issue_bykey import issue_bykey

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "success_tool.settings")
django.setup()

def issue_list_data(request):
    payload = construct_payload(request)
    url = os.getenv('JIRA_URL')
    response = requests.post(url, headers=headers, auth=auth, data=json.dumps(payload), verify=True)
    data_list = []
    json_file_path = "E:/IFS_BACKEND/success_tool_backend_local/report_creaton/apps/utility/findproductcap.json"
    with open(json_file_path, "r", encoding='utf-8') as json_file:
        data = json.load(json_file) 
    #if response.status_code == 200:
    if True:
        #issues_data = json.loads(response.text)
        issues_data = data
        total_records = issues_data['total']
        menuList = list(MenuCardMaster.objects.values_list('menu_card', flat=True))

        for issue in issues_data['issues']:
            menu_card = None
            partner = False
            menu_description = ''
            customer_id = ''
            changelog = issue.get("changelog", {}).get("histories", [])
            changelog_assignee_created = None
            
            subtasks = issue["fields"].get('subtasks', [])
            subtasks_list = extract_subtasks_data(subtasks)

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
            parent_id = issue["fields"]["parent"].get("id", "") if "parent" in issue["fields"] else None
            parent_key = issue["fields"]["parent"].get("key", "") if "parent" in issue["fields"] else None
            parent_summary = issue["fields"]["parent"]["fields"].get('summary', "") if "parent" in issue["fields"] else None

            activity_short_name = issue["fields"].get("customfield_16036", "")
            if activity_short_name and '.' in activity_short_name:
                activity_split_string = activity_short_name.split('.')
                activit_project_id = activity_split_string[0]
                activit_menu_string = activity_split_string[2]
                menu_card, partner = find_menuid_in_string(activit_menu_string, menuList)

            if menu_card is None:
                menu_card, partner = find_menuid_in_string(issue_summary, menuList)

            if menu_card is None:
                menu_card, partner = find_menuid_in_string(parent_summary, menuList)

            if menu_card is None and subtasks is True:
                parent_activity_string = issue_bykey(parent_key)
                if parent_activity_string:
                    parent_activity_name = parent_activity_string.split('.')
                    parent_activit_id = parent_activity_name[0]
                    menu_card, partner = find_menuid_in_string(parent_activit_id, menuList)

            changelog_assignee_created = convert_date(changelog_assignee_created)
            project_id = issue["fields"]["project"].get("id", "")
            project_name = issue["fields"]["project"].get("name", "")
            project_key = issue["fields"]["project"].get("key", "")
            customer_id = project_key[2:]
            subtask = issue["fields"]["issuetype"].get("subtask", "")
            assignee_name = issue["fields"]["assignee"].get("displayName", "") if "assignee" in issue["fields"] else None
            
            issue_fields = {
                "issue_key": issue_key,
                "issue_summary": issue_summary,
                "menu_card": menu_card,
                "customer_id": customer_id,
                "subtasks_list": subtasks_list,
                "partner": partner,
                "subtask": subtask,
                "project_id": project_id,
                "project_key": project_key,
                "project_name": project_name,
                "issue_id": issue_id,
                "created_date": created,
                "assign_date": changelog_assignee_created if changelog_assignee_created else None,
                "parent_id": parent_id,
                "parent_key": parent_key,
                "assignee_name": assignee_name
            }

            data_list.append(issue_fields)

        for dt in data_list:
            menu_card_id = dt.get('menu_card')
            customer_id = dt.get('customer_id')
            issue_key = dt.get('issue_key')
            
            menu_card_data = MenuCardMaster.objects.filter(menu_card=menu_card_id, status=1).first()
            report_data = SuccessReport.objects.filter(jira_key=issue_key, status=1).first()
            customer_map = CustomerMapping.objects.filter(customer__customer_id=customer_id, status=1).first()
            sdo_map = MenuSdoMapping.objects.filter(menu_card__menu_card=menu_card_id, status=1, sdo__status=1).first()
            if sdo_map:
                dt['sdo_name'] = sdo_map.sdo.sdo_name if sdo_map.sdo else ''
                
            if report_data:
                dt['report_status'] = str(report_data.report_status.id)
                dt['report_error'] = report_data.error_msg
                dt['download_link'] = report_data.download_link
            else:
                dt['report_status'] = '1'

            if menu_card_data is not None:
                dt['menu_description'] = menu_card_data.menu_description
            if customer_map:
                dt['csm_name'] = customer_map.csm.csm_name if customer_map.csm else ''
                dt['sdm_name'] = customer_map.sdm.sdm_name if customer_map.sdm else ''
                dt['psm_name'] = customer_map.psm.psm_name if customer_map.psm else ''

        return data_list, total_records
    else:
        return [], 0
