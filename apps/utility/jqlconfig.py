# jqlconfig.py
from requests.auth import HTTPBasicAuth
import os

# Configure headers for the Jira API request
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Configure authentication credentials
auth = HTTPBasicAuth(os.getenv('JIRA_EMAIL'), os.getenv('JIRA_TOKEN'))
