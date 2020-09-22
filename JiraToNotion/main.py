from response_parser.jira_response_parser import parse_query_specific_ticket

if __name__ == '__main__':
    test = parse_query_specific_ticket("CBUPT-7250")
    print(test.link)
