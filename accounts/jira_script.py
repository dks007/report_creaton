# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
from requests.auth import HTTPBasicAuth
import json

def jira():
    url = "https://dsklocal.atlassian.net/rest/api/2/events"
    to = "ATATT3xFfGF0WfP3Y8T7h2hbqpXAlogMNENL-QvKeL5O5kLXnhNc9UGZLYolR6Inat3HOE_wy1Wx_LhvU-xyVG_4oEs4R3_3cpe2FTduvpKenzUnuMNd4K65tyFAY08-gKDsXovOiy5Ako154-3fgFQ1JTjMG1bwx7nB9tiRuvS8hdLIGjx5wdU=4E400EA8"

    auth = HTTPBasicAuth('dilip.ku.007@gmail.com', to)

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
