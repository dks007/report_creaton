# jqlpayload.py
import os
from datetime import datetime

# Construct payload for the Jira API request
def listing_construct_payload(request):
    
    startAt = int(request.GET.get('start', 0))  # Default value: 0
    maxResults = int(request.GET.get('max_result', 20))  # Default value: 20
    filterByCreatedDate = request.GET.get('filterByCreatedDate', False)  # Default value: False
    startDate = request.GET.get('startDate')
    endDate = request.GET.get('endDate')
    sortBy = request.GET.get('sortBy', 'created')  # Default value: 'created'
    order = request.GET.get('order', 'DESC')  # Default value: 'DESC'
    #issuetype = request.GET.get('issuetype', 'Tasks')  # Default value: 'Sub-task, Task'
    #issuetype = request.GET.get('issuetype', 'Sub-task, Tasks')  # Default value: 'Sub-task, Task'
    issuekey = request.GET.get('issuekey', '')  # Filter by Issue Key
    status = request.GET.get('status', "('Awaiting Customer', 'In Process', 'In Review', 'Not Started')")  # Default value for status
    parent_key = request.GET.get('parent_key', '')  # Filter by parent Key
    activity_key_field = request.GET.get('activity_shname', 'True') # for activity short name customfield_16036

    jql_parts = []

    if parent_key:
        jql_parts.append(f"parent in ({parent_key})")
        issuetype = request.GET.get('issuetype', 'Sub-task, Tasks')

    else:
        issuetype = request.GET.get('issuetype', 'Tasks')

    if issuetype:
        jql_parts.append(f"issuetype in ({issuetype})")


    if issuekey:
        jql_parts.append(f"key in ({issuekey})")

    if filterByCreatedDate == 'True' and startDate and endDate:
        start_date_str = datetime.strptime(startDate, "%Y-%m-%d").strftime("%Y-%m-%d")
        end_date_str = datetime.strptime(endDate, "%Y-%m-%d").strftime("%Y-%m-%d")
        jql_parts.append(f"created >= '{start_date_str}' AND created <= '{end_date_str}'")

    if status:
        jql_parts.append(f"status in {status}")

    if activity_key_field =='True':
        jql_parts.append(f"cf[16036] IS NOT EMPTY")

    jql_parts.append("'Service Category[Dropdown]' = 'Expert Services'")
    jql_parts.append("assignee NOT in (EMPTY)")
    # for activity short name filter 
    #jql_parts.append("customfield_16036 NOT in (EMPTY)")

    # Joining all JQL parts with AND and adding order by clause
    jql_query = " AND ".join(jql_parts) + f" order by {sortBy} {order}"

    payload = {
        "expand": ["changelog"],
        "jql": jql_query,
        "fieldsByKeys": False,
        "fields": [
            "summary", "description", "project", "customfield_16032",
            "customfield_16015", "customfield_16036", "customfield_16262",
            "customfield_16263", "customfield_16264", "customfield_16265",
            "customfield_16266", "assignee", "issuetype", "status",
            "parent", "created", "creator", "subtasks", "comment"
        ],
        "maxResults": maxResults,
        "startAt": startAt
    }

    print("payload--->",payload)

    return payload
