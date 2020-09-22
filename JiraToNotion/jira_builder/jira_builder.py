from models.sprint import Sprint
from models.jira_config import Jira_Config
from constants.constants import JIRA_API_JQL_URL, JIRA_API_EVAL_URL, JIRA_API_BASE_REPLACE, FOLDER_DATA, FOLDER_DATA_FILE, FOLDER_DATA_FILE_REPLACE, FILE_SPRINT_DATA, FILE_TICKETS_DATA, FOLDER_CONFIG_FILE, FOLDER_CONFIG_FILE_REPLACE, FILE_JIRA_CONFIG
import json
import os
import requests
from requests.auth import HTTPBasicAuth


# Public Methods

def query_active_sprints():
    jira_config = Jira_Config()

    query = json.dumps({
        "expression": "{active_sprints: board.activeSprints}",
        "context": {
            "board": jira_config.board_number
        }
    })

    return __make_jira_query_request(query)


def query_issues_for_sprint(sprint):
    jql_sprint = "sprint = " + str(sprint)
    jql = json.dumps({
        "jql": jql_sprint,
        "fields": [
            "summary",
            "status",
            "assignee",
            "comment"
        ]
    })

    return __make_jira_jql_request(jql)

def query_specific_issue(issue_name):
    jql_issue = "issue = " + issue_name
    jql = json.dumps({
        "jql": jql_issue,
        "fields": [
            "summary",
            "created",
            "assignee",
            "reporter",
            "subtasks"
        ]
    })

    return __make_jira_jql_request(jql)

# Private methods

def __make_jira_jql_request(jql):
    jira_config = Jira_Config()

    api = JIRA_API_JQL_URL.replace(
        JIRA_API_BASE_REPLACE, jira_config.jira_cloud_base)

    auth = HTTPBasicAuth(jira_config.username, jira_config.token)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = jql

    try:
        response = requests.request(
            "POST",
            api,
            data=payload,
            headers=headers,
            auth=auth
        )

        if not os.path.exists(FOLDER_DATA):
            os.makedirs(FOLDER_DATA)

        # Write the sprint data to the data directory
        write_file = FOLDER_DATA_FILE.replace(
            FOLDER_DATA_FILE_REPLACE, FILE_TICKETS_DATA)
        with open(write_file, 'w') as outfile:
            json.dump(response.text, outfile)

    except Exception as e:
        print('Something went wrong with requesting sprint information. Is your board # correct?')
        print(e)

    return json.loads(response.text)


def __make_jira_query_request(query):
    jira_config = Jira_Config()

    api = JIRA_API_EVAL_URL.replace(
        JIRA_API_BASE_REPLACE, jira_config.jira_cloud_base)

    auth = HTTPBasicAuth(jira_config.username, jira_config.token)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = query

    try:
        response = requests.request(
            "POST",
            api,
            data=payload,
            headers=headers,
            auth=auth
        )

        # Create a data directory if it doesnt exist
        if not os.path.exists(FOLDER_DATA):
            os.makedirs(FOLDER_DATA)

        # Write the sprint data to the data directory
        write_file = FOLDER_DATA_FILE.replace(
            FOLDER_DATA_FILE_REPLACE, FILE_SPRINT_DATA)
        with open(write_file, 'w') as outfile:
            json.dump(response.text, outfile)

    except Exception as e:
        print('Something went wrong with requesting sprint information. Is your board # correct?')
        print(e)

    return json.loads(response.text)
