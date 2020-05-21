from config_builder.config_builder import get_file_data
from models.sprint import Sprint
from models.jira_config import Jira_Config
from constants.constants import JIRA_API_EVAL_URL, JIRA_API_BASE_REPLACE, FOLDER_DATA, FOLDER_DATA_FILE, FOLDER_DATA_FILE_REPLACE, FILE_SPRINT_DATA, FOLDER_CONFIG_FILE, FOLDER_CONFIG_FILE_REPLACE, FILE_JIRA_CONFIG
import json
import os
import requests
from requests.auth import HTTPBasicAuth


def make_jira_query_request(query):
    jira_config = __get_jira_config_data()

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


def query_active_sprints():
    jira_config = __get_jira_config_data()

    query = json.dumps({
        "expression": "{active_sprints: board.activeSprints}",
        "context": {
            "board": jira_config.board_number
        }
    })

    return make_jira_query_request(query)


def __get_jira_config_data():
    try:
        jira_config = FOLDER_CONFIG_FILE.replace(
            FOLDER_CONFIG_FILE_REPLACE, FILE_JIRA_CONFIG)
        config_path = os.path.abspath(jira_config)
        jira_data = get_file_data(config_path)
        config = Jira_Config(jira_data)
    except:
        print("Unable to locate the jira_config.json file. do you ahve one created in the root of the directory?")

    return config
