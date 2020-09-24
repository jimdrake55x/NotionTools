from models.ticket import Ticket


def ticket_collection_scheme(tickets: [Ticket]):
    labelOptions = __labels_schema(tickets)
    statusOptions = __status_schema(tickets)
    ticketTypeOptions = __ticket_type_schema(tickets)

    return {
        'BrbY': {'name': 'Assignee', 'type': 'text'},
        'M<X_': {'name': 'Ticket Link', 'type': 'url'},
        'T~rI': {'name': 'Reporter', 'type': 'text'},
        'dcdI': {'name': 'Created Date', 'type': 'date'},
        'jpRx': {'name': 'Pull Request', 'type': 'url'},
        'lHq{': {
            'name': 'Ticket Type',
            'type': 'select',
            'options': ticketTypeOptions,
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


def __labels_schema(tickets: [Ticket]):
    options = []
    labels = []
    for ticket in tickets:
        for label in ticket.labels:
            if label not in labels:
                labels.append(label)
                options.append({
                    "color": "default",
                    "id": "this-is-the-id-for-{0}".format(label),
                    "value": label,
                })

    return options


def __status_schema(tickets: [Ticket]):
    options = []
    status = []
    for ticket in tickets:
        if ticket.status not in status:
            status.append(ticket.status)
            options.append({
                "color": "default",
                "id": "this-is-the-id-select-{0}".format(ticket.status),
                "value": ticket.status,
            })

    return options


def __ticket_type_schema(tickets: [Ticket]):
    options = [
        {
            "color": "default",
            "id": "this-is-id-for-type-{0}".format("Task"),
            "value": "Task"
        }
    ]
    return options
