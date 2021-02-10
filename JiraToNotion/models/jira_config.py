from constants.constants import FOLDER_CONFIG_FILE, FOLDER_CONFIG_FILE_REPLACE, FILE_JIRA_CONFIG
from config_builder.config_builder import get_file_data
import os



class Jira_Config():

    def __init__(self):
        try:
            jira_config = FOLDER_CONFIG_FILE.replace(
                FOLDER_CONFIG_FILE_REPLACE, FILE_JIRA_CONFIG)
            config_path = os.path.abspath(jira_config)
            jira_data = get_file_data(config_path)
        except:
            print("Unable to locate the jira_config.json file. do you have one created in the root of the directory?")

        self.username = jira_data['username']
        self.token = jira_data['token']
        self.board_number = jira_data['board_number']
        self.jira_cloud_base = jira_data['jira_cloud_base']
        self.jira_sort_property_id = jira_data['jira_sort_property_id']
