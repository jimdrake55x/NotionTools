from config_builder.config_builder import get_file_data
from models.sprint import Sprint
from constants.constants import JIRA_SPRINTS_URL, JIRA_SPRINTS_URL_PROJECT_REPLACE, FOLDER_DATA, FOLDER_DATA_FILE, FOLDER_DATA_FILE_REPLACE, FILE_SPRINT_DATA, FOLDER_CONFIG_FILE, FOLDER_CONFIG_FILE_REPLACE, FILE_JIRA_CONFIG
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
        if not os.path.exists(FOLDER_DATA):
            os.makedirs(FOLDER_DATA)

        # Write the sprint data to the data directory
        write_file = FOLDER_DATA_FILE.replace(
            FOLDER_DATA_FILE_REPLACE, FILE_SPRINT_DATA)
        with open(write_file, 'w') as outfile:
            json.dump(response, outfile)

    except Exception as e:
        print('Something went wrong with requesting sprint information. Is your board # correct?')
        print(e)

    return response


def get_jira_config_data():
    try:
        jira_config = FOLDER_CONFIG_FILE.replace(
            FOLDER_CONFIG_FILE_REPLACE, FILE_JIRA_CONFIG)
        config_path = os.path.abspath(jira_config)
        jira_data = get_file_data(config_path)
    except:
        print("Unable to locate the jira_config.json file. do you ahve one created in the root of the directory?")

    return jira_data
