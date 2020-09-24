from models.ticket import Ticket
from constants.theme import Theme
from models.notion_config import Notion_config
from constants.collection_types import Collection_Type
from notion_builder.collection_builder import create_ticket_collection, add_tickets_to_collection


def test_insert_page(tickets: [Ticket]):
    col = create_ticket_collection("Tickets", [Collection_Type.TABLE], tickets)
    add_tickets_to_collection(tickets, Theme.LIGHT, col)
