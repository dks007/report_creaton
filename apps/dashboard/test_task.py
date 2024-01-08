# success_tool/test_tasks.py
from tasks import fetch_and_save_jira_data


def test_fetch_and_save_jira_data():
    result = fetch_and_save_jira_data.delay()
    result_status = result.status
    assert result_status == 'PENDING'
