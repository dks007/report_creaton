# jqlpayload.py
import os
from datetime import datetime

# Construct custome payload query for the Jira API request
def custome_query_payload(issueKey,fieldKey='customfield_16036'):
    issueKey = fieldKey  # Filter by Issue Key
    payload = {
        "jql": f" key in {fieldKey} AND 'Service Category[Dropdown]' = 'Expert Services' AND assignee NOT in (EMPTY)",
        "fieldsByKeys": False,
        "fields": [
            fieldKey
        ]
    }

    if issueKey is not None:
        payload['jql'] = f"key in {issueKey}"

    return payload
