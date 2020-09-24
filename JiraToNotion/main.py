from notion_builder.notion_builder import test_insert_page
from jira.jira import get_specific_ticket, get_active_sprint_id, get_tickets_for_sprint

if __name__ == '__main__':
    print("Getting active Sprint Id...")
    sprintId = get_active_sprint_id()[0]
    print(
        "Active Sprint Id: {0}...\nGetting tickets for sprint...".format(sprintId.number))
    tickets = get_tickets_for_sprint(sprintId.number)

    print("inserting tickets into notion...")
    test_insert_page(tickets)
    print("Done with tickets...")
