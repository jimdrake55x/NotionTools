from notion.client import NotionClient
from notion.block import TodoBlock, CollectionViewBlock
from config_builder.config_builder import get_file_data
from models.ticket import Ticket
import json
import os


def test_insert_page(ticket: Ticket):

    notion_config_data = load_notion_configs()
    token = notion_config_data['token']
    base_page = notion_config_data['base_page']
    theme = notion_config_data['theme']

    icon = "https://img.icons8.com/ios/250/000000/source-code.png"
    if theme == "DARK":
        icon = "https://img.icons8.com/ios/250/FFFFFF/source-code.png"

    # client
    client = NotionClient(token_v2=token)

    # Page to edit
    page = client.get_block(base_page)

    # Add a new Collection
    collection = page.children.add_new(CollectionViewBlock)
    collection.collection = client.get_collection(
        client.create_record("collection", parent=collection, schema=__ticket_collection_scheme())
    )
    collection.title = "Tickets"
    view = collection.views.add_new(view_type="table")
    



def load_notion_configs():
    try:
        config_path = os.path.abspath(
            './JiraToNotion/configs/notion_config.json')
        notion_data = get_file_data(config_path)
    except:
        print("Unable to locate the notion_config.json file. do you have one created in the root of the directory?")

    return notion_data


def __ticket_collection_scheme():
    return {
        'BrbY': {'name': 'Assignee', 'type': 'text'}, 
        'M<X_': {'name': 'Ticket Link', 'type': 'url'}, 
        'T~rI': {'name': 'Reporter', 'type': 'text'}, 
        'dcdI': {'name': 'Created Date', 'type': 'date'}, 
        'jpRx': {'name': 'Pull Request', 'type': 'url'}, 
        'lHq{': {'name': 'Ticket Type', 'type': 'select'}, 
        'oJ{W': {'name': 'Ticket Lables', 'type': 'multi_select'}, 
        'title': {'name': 'Ticket Name', 'type': 'title'}
    }
