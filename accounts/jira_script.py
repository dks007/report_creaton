# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
from requests.auth import HTTPBasicAuth
import json
import os

def jira():
    url = "https://dsklocal.atlassian.net/rest/api/2/events"
    token = os.getenv("TOKEN")
    email = os.getenv("EMAIL")

    auth = HTTPBasicAuth(email, token)

    headers = {
        "Accept": "application/json",
        # "Content-Type": "application/json"
    }
    payload = json.dumps({
        "emailAddress": "shan@gmail.com"
    })
    query = {
        'accountId': '557058:bdad8705-a148-4fab-b50f-c98d5c5d3a3c'
    }

    response = requests.request(
        "GET",
        # "POST",
        url,
        headers=headers,
        # params=query,
        # data=payload,
        auth=auth
    )

    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

    return response.text
