from jira.jira import get_specific_ticket, get_active_sprint_id, get_tickets_for_sprint


def print_notes(print_all_tickets):
    print("=== Start of Notes ===")

    tickets = get_tickets_for_sprint(get_active_sprint_id()[0].number)

    if not print_all_tickets:
        tickets = list(filter(lambda x: x.status.status != "Done", tickets))

    for ticket in tickets:
        stringToPrint = "{0}: {1}".format(ticket.title, ticket.summary)

        # Strike through if the task is done
        if(ticket.status.status == "Done"):
            stringToPrint = "~" + stringToPrint + "~ ✅"
        else:
            stringToPrint = stringToPrint + " :in-progress:"

        # Bold it
        stringToPrint = "*" + stringToPrint + "*"
        print(stringToPrint)
        print("\n")

    print("=== End of Notes ===")
