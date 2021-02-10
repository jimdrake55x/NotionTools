from constants.constants import FOLDER_CONFIG_FILE, FOLDER_CONFIG_FILE_REPLACE, FILE_NOTION_CONFIG
from config_builder.config_builder import get_file_data
import os


class Notion_config():

    def __init__(self):
        try:
            notion_config = FOLDER_CONFIG_FILE.replace(
                FOLDER_CONFIG_FILE_REPLACE, FILE_NOTION_CONFIG)
            config_path = os.path.abspath(notion_config)
            notion_data = get_file_data(config_path)
        except:
            print("Unable to locate the notion_config.json file. do you have one created in the root of the directory?")

        self.token = notion_data['token']
        self.base_page = notion_data['base_page']
        self.theme = notion_data['theme']
