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
from .jql_query import custome_query_payload
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "success_tool.settings")
django.setup()

def issue_bykey(filterKey):
    """
    Fetches issue data from Jira API and populates by issue key.

    Args:
        issue_key (str): jira issue key

    Returns:
        tuple: response data provide individual records of issue key.
    """
    url = os.getenv('JIRA_URL')
     # Getting request
    emailId = "dilip.kumar.shrivastwa@ifs.com"
    # Construct payload using jqlpayload.py
    payload_custome = custome_query_payload(filterKey)
   
    # Send request to Jira API
    response = requests.request(
        "POST",
        url,
        headers=headers,
        auth=auth,
        data=json.dumps(payload_custome),
        verify=False
    )

    if response.status_code == 200:
        issue_data = json.loads(response.text)
        #total_records = issue_data['total']
        issue = issue_data['issues'][0]  # Extracting the single issue            
        #issue_key = issue.get("key", "")
        #parent_id = issue["fields"]["parent"].get("id", "") if "parent" in issue["fields"] else None
        #parent_key = issue["fields"]["parent"].get("key", "") if "parent" in issue["fields"] else None
        activity_short_name = issue["fields"].get("customfield_16036", None)
        # Create an Issue instance
        
        return  activity_short_name # Returning a list with a single record and total count

    else:
        None
