from models.notion_config import Notion_config
from notion.client import NotionClient
from notion.block import TodoBlock, CollectionViewBlock, HeaderBlock, DividerBlock, TextBlock
from notion.collection import NotionDate
from constants.collection_types import Collection_Type
from notion_builder.schema_builder import ticket_collection_scheme
from models.ticket import Ticket
from constants.theme import Theme
from constants.icons import Icon
from utilities.icon_builder import get_icon


def get_page_title(page):

    # Get notion config
    notion_config = Notion_config()

    client = NotionClient(token_v2=notion_config.token)
    page = client.get_block(page)

    return page.title


def create_ticket_collection(title, views: [Collection_Type], tickets: [Ticket]):

    # Get notion config settings
    notion_config = Notion_config()

    # Set up client and get page to work on
    client = NotionClient(token_v2=notion_config.token)
    page = client.get_block(notion_config.base_page)

    # Add a new collection
    collection = page.children.add_new(CollectionViewBlock)

    collection.collection = client.get_collection(
        client.create_record("collection", parent=collection,
                             schema=ticket_collection_scheme(tickets))
    )

    collection.title = title

    # Add desired Views
    for view in views:
        collection.views.add_new(view_type=view.value)

    return collection


def add_tickets_to_collection(tickets: [Ticket], theme: Theme, collection):
    icon = get_icon(Icon.DEV, theme)

    for ticket in tickets:
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
        newRow.status = ticket.status.status
        newRow.ticket_type = ticket.ticket_type

        __add_ticket_summary(ticket, newRow)


def __add_ticket_summary(ticket: Ticket, row):
    row.children.add_new(HeaderBlock, title="Summary")
    row.children.add_new(TextBlock, title=ticket.summary)
    row.children.add_new(HeaderBlock, title="Testing")
    row.children.add_new(TodoBlock, title="*Testing notes go here...*")
    row.children.add_new(DividerBlock)
    row.children.add_new(HeaderBlock, title="Work Notes")
