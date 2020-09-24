from response_parser.jira_response_parser import parse_query_specific_ticket
from notion_builder.notion_builder import test_insert_page

if __name__ == '__main__':
    print("Fetching Jira information for CBUPT-7250...")
    test = parse_query_specific_ticket("CBUPT-7250")
    test = [test]
    print("Creating ticket for CBUPT-7250...")
    test_insert_page(test)
    print("Done with CBUPT-7250...")
