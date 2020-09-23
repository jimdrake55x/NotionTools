from notion.client import NotionClient
from notion.block import TodoBlock, CollectionViewBlock
from notion.collection import NotionDate
from config_builder.config_builder import get_file_data
from models.ticket import Ticket
import datetime
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

    # Get options for the labels
    labelOptions = __labels_schema(ticket)
    statusOptions = __status_schema(ticket)
    typeOptions = __ticket_type_schema(ticket)

    collection.collection = client.get_collection(
        client.create_record("collection", parent=collection,
                             schema=__ticket_collection_scheme(labelOptions, statusOptions, typeOptions))
    )
    collection.title = "Tickets"
    view = collection.views.add_new(view_type="table")

    # Add a new row
    newRow = collection.collection.add_row()
    newRow.ticket_name = ticket.key
    newRow.icon = icon
    newRow.assignee = ticket.assignee.username
    newRow.reporter = ticket.reporter.username
    newRow.created_date = NotionDate(start=ticket.created_date)
    newRow.ticket_link = ticket.link

    # Add Labels
    labels = []
    for label in ticket.labels:
        labels.append(label)
    newRow.ticket_labels = labels

    # Add Status
    newRow.status = ticket.status
    newRow.ticket_type = "Task"


def load_notion_configs():
    try:
        config_path = os.path.abspath(
            './JiraToNotion/configs/notion_config.json')
        notion_data = get_file_data(config_path)
    except:
        print("Unable to locate the notion_config.json file. do you have one created in the root of the directory?")

    return notion_data


def __ticket_collection_scheme(labelOptions, statusOptions, typeOptions):
    return {
        'BrbY': {'name': 'Assignee', 'type': 'text'},
        'M<X_': {'name': 'Ticket Link', 'type': 'url'},
        'T~rI': {'name': 'Reporter', 'type': 'text'},
        'dcdI': {'name': 'Created Date', 'type': 'date'},
        'jpRx': {'name': 'Pull Request', 'type': 'url'},
        'lHq{': {
            'name': 'Ticket Type',
            'type': 'select',
            'options': typeOptions,
        },
        'oJ{W': {
            'name': 'Ticket Labels',
            'type': 'multi_select',
            'options': labelOptions
        },
        'AnKr': {
            'name': 'Status',
            'type': 'select',
            'options': statusOptions
        },
        'title': {'name': 'Ticket Name', 'type': 'title'}
    }


def __labels_schema(ticket: Ticket):
    options = []
    for label in ticket.labels:
        options.append({
            "color": "default",
            "id": "this-is-the-id-for-{0}".format(label),
            "value": label,
        })
    return options


def __status_schema(ticket: Ticket):
    option = [{
        "color": "default",
        "id": "this-is-the-id-select-{0}".format(ticket.status),
        "value": ticket.status,
    }]
    return option


def __ticket_type_schema(ticket: Ticket):
    options = [
        {
            "color": "default",
            "id": "this-is-id-for-type-{0}".format("Task"),
            "value": "Task"
        }
    ]
    return options
