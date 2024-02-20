# jqlpayload.py
import os
from datetime import datetime
# Construct payload for the Jira API request
def construct_payload(request,id=None):
    issueKey = id  # Filter by Issue Key
    payload = {
        "expand": ["changelog"],
        "jql": f"key in ({issueKey}) AND status in ('Awaiting Customer', 'In Process','In Review','Not Started') AND 'Service Category[Dropdown]' = 'Expert Services' AND assignee NOT in (EMPTY)",
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
            "customfield_16266",
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

    return payload
