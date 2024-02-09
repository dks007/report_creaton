# jqlpayload.py
import os
from datetime import datetime

# Construct payload for the Jira API request
def construct_payload(request):
    startAt = int(request.GET.get('start', 0))  # Default value: 0
    maxResults = int(request.GET.get('max_result', 20))  # Default value: 20
    filterByCreatedDate = request.GET.get('filterByCreatedDate', False)  # Default value: False
    startDate = request.GET.get('startDate')
    endDate = request.GET.get('endDate')
    sortBy = request.GET.get('sortBy', 'created')  # Default value: 'created'
    order = request.GET.get('order', 'DESC')  # Default value: 'DESC'
    issueType = request.GET.get('issueType', 'Sub-task, Tasks')  # Default value: 'Sub-task, Task'
    issueKey = request.GET.get('issueKey', None)  # Filter by Issue Key
    status = request.GET.get('status', "('Awaiting Customer', 'In Process','In Review','Not Started')")  # Default value: "('Awaiting Customer', 'In Process','In Review','Not Started')"

    payload = {
        "expand": ["changelog"],
        "jql": f"issuetype in ({issueType}) AND status in {status} AND 'Service Category[Dropdown]' = 'Expert Services' AND assignee NOT in (EMPTY) order by {sortBy} {order}",
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
        ]
    }

    if issueKey is not None:
        payload['jql'] = f"key in {issueKey}"

    if filterByCreatedDate and startDate and endDate:
        start_date_str = datetime.strptime(startDate, "%Y-%m-%d").strftime("%Y-%m-%d")
        end_date_str = datetime.strptime(endDate, "%Y-%m-%d").strftime("%Y-%m-%d")
        payload['jql'] = f"created >= '{start_date_str}' AND created <= '{end_date_str}'"

    payload['maxResults'] = maxResults
    payload['startAt'] = startAt

    return payload
