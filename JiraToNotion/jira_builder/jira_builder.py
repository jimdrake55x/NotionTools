from config_builder.config_builder import get_file_data
from models.sprint import Sprint
from constants.constants import JIRA_SPRINTS_URL, JIRA_SPRINTS_URL_PROJECT_REPLACE
import json
import os
import requests


def make_sprint_requests():
    jira_data = get_jira_config_data()
    username = jira_data['username']
    token = jira_data['token']
    project_number = jira_data['project_number']

    api = JIRA_SPRINTS_URL.replace(
        JIRA_SPRINTS_URL_PROJECT_REPLACE, project_number)

    try:
        # Fetch sprints from Jira
        response = requests.get(api, auth=(username, token)).json()

        # Create a data directory if it doesnt exist
        if not os.path.exists('./JiraToNotion/data/'):
            os.makedirs('./JiraToNotion/data/')

        # Write the sprint data to the data directory
        with open('./JiraToNotion/data/data_sprint.json', 'w') as outfile:
            json.dump(response, outfile)

    except Exception as e:
        print('Something went wrong with requesting sprint information. Is your board # correct?')
        print(e)

    return response


def get_jira_config_data():
    try:
        config_path = os.path.abspath(
            './JiraToNotion/configs/jira_config.json')
        jira_data = get_file_data(config_path)
    except:
        print("Unable to locate the jira_config.json file. do you ahve one created in the root of the directory?")

    return jira_data
