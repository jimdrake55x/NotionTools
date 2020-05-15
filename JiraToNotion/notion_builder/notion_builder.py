from notion.client import NotionClient
from notion.block import TodoBlock
import json
import os


def say_hello():
    print("Hello, world!")


def test_insert_page():

    notion_config_data = load_notion_configs()
    token = notion_config_data['token']
    base_page = notion_config_data['base_page']

    # client
    client = NotionClient(token_v2=token)

    # Page to edit
    page = client.get_block(base_page)

    print("The current title is:", page.title)

    page.title = "The title is changed"


def load_notion_configs():
    try:
        config_path = os.path.abspath(
            './JiraToNotion/configs/notion_config.json')
        notion_data = get_notion_data(config_path)
    except:
        print("Unable to locate the notion_config.json file. do you ahve one created in the root of the directory?")

    return notion_data


def get_notion_data(config_file):
    with open(config_file) as config:
        data = json.load(config)

    return data
