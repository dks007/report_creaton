# success_tool/tasks.py
from celery import shared_task
from datetime import datetime
from requests.auth import HTTPBasicAuth
import json
import requests
import time
from django.conf import settings
from apps.dashboard.models import Issue


@shared_task
def fetch_and_save_jira_data():
    url = "https://ifsdev.atlassian.net/rest/api/3/search"
    auth = HTTPBasicAuth("dilip.kumar.shrivastwa@ifs.com",
                         "ATATT3xFfGF0p-FG8-lj6HsWs80g3AtzRePPZ4WDbZEq_ZlDJoEVV3zcusdMdiyGxn1do8ldFe4Tgy4OcC2gOc9yArvRSzZ24z13JqWPxKsJvvinVybUIwYdlnla8QErcuYl0XnMBvLc_Fn_sk2TntBf1Rj4DZ-hkL5FOr4xu5kDo9M2rna2vEQ=B3F4BE74")

    max_duration_seconds = 60
    start_time = time.time()
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # set the initial parameters
    payload = {
        "expand": [
            "changelog"
        ],
        "jql": "issuetype in (Sub-task, Tasks) AND status in ('Awaiting Customer', 'In Process','In Review','Not Started') AND 'Service Category[Dropdown]' = 'Expert Services' AND assignee NOT in (EMPTY) order by created DESC",
        "fieldsByKeys": False,
        "fields": [
            "summary",
            "project",
            "customfield_16036",
            "assignee",
            "issuetype",
            "status",
            "parent",
            "created",
            "creator"
        ],
        "maxResults": 100,
        "startAt": 0
    }

    # Use default database configuration from settings.py
    db_config = {
        "host": settings.DATABASES['default']['HOST'],
        "user": settings.DATABASES['default']['USER'],
        "password": settings.DATABASES['default']['PASSWORD'],
        "database": settings.DATABASES['default']['NAME'],
    }

    while True:
        response = requests.request(
            "POST",
            url,
            headers=headers,
            auth=auth,
            data=json.dumps(payload),
            verify=False
        )

        # check if the request response was successful
        if response.status_code == 200:
            # parse the JSON
            issues_data = json.loads(response.text)

            # Insert data into Django model
            for issue in issues_data['issues']:
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

                summary = issue["fields"].get('summary', "")
                issue_id = issue.get("id", "")
                issue_key = issue.get("key", "")
                created = issue["fields"].get('created', "")
                changelog_assignee_created = changelog_assignee_created
                creator_email = issue["fields"]["creator"].get("emailAddress", "") if "creator" in issue[
                    "fields"] else None
                project = issue["fields"]["project"].get("name", "")
                parent_key = issue["fields"]["parent"].get("key", "") if "parent" in issue["fields"] else None
                parent_summary = issue["fields"]["parent"]["fields"].get('summary', "") if "parent" in issue[
                    "fields"] else None
                project_key = issue["fields"]["project"].get("key", "")
                subtask = issue["fields"]["issuetype"].get("subtask", "")
                customfield_16036 = issue["fields"].get("customfield_16036", "")
                assignee_email = issue["fields"]["assignee"].get("emailAddress", "") if "assignee" in issue[
                    "fields"] else None
                status = issue["fields"]["status"].get("name", "")

                # Create an Issue instance
                new_issue = Issue(
                    summary=summary,
                    issue_id=issue_id,
                    issue_key=issue_key,
                    created=created,
                    changelog_assignee_created=changelog_assignee_created,
                    creator_email=creator_email,
                    project=project,
                    parent_key=parent_key,
                    parent_summary=parent_summary,
                    project_key=project_key,
                    subtask=subtask,
                    customfield_16036=customfield_16036,
                    assignee_email=assignee_email,
                    status=status
                )

                # Save the instance to the database
                new_issue.save()

            # check if there are more issues to retrieve
            if time.time() - start_time > max_duration_seconds:
                print("time exceeds!")
                break
            if issues_data['startAt'] + issues_data['maxResults'] < issues_data['total']:
                # increment the startAt parameter for next
                payload['startAt'] += issues_data['maxResults']
                print(payload['startAt'])
            else:
                # all issues have been retrieved
                break

        else:
            # print error if the request was not successful
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            # print(response.text)
            break

    print("Data has been successfully inserted into the MySQL database.")
