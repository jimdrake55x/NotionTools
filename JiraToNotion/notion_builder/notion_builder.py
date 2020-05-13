from notion.client import NotionClient


def say_hello():
    print("Hello, world!")


def test_insert_page():
    # client
    client = NotionClient(
        token_v2="Token Goes here)

    # Page to edit
    page = client.get_block(
        "https://www.notion.so/Test-Page-please-ignore-eb59a27d75394487a048e3fa05d3751a")

    print("The old title is:", page.title)

    page.title = "The title is changed, GET USED TO IT"
