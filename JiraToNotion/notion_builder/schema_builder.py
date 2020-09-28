from models.ticket import Ticket
import random


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
                    "color": __get_random_color(),
                    "id": "this-is-the-id-for-{0}".format(label),
                    "value": label,
                })

    return options


def __status_schema(tickets: [Ticket]):
    options = []
    status = []
    for ticket in tickets:
        if ticket.status.status not in status:
            status.append(ticket.status.status)
            options.append({
                "color": ticket.status.color,
                "id": "this-is-the-id-select-{0}".format(ticket.status.status),
                "value": ticket.status.status,
            })

    return options


def __ticket_type_schema(tickets: [Ticket]):
    options = []
    types = []
    for ticket in tickets:
        if ticket.ticket_type not in types:
            types.append(ticket.ticket_type)
            options.append(
                {
                    "color": __get_random_color(),
                    "id": "this-is-id-for-type-{0}".format(ticket.ticket_type),
                    "value": ticket.ticket_type
                })
    return options


def __get_random_color():
    colors = ["default", "gray", "brown", "orange",
              "yellow", "green", "blue", "purple", "pink", "red"]
    randomColor = random.randint(0, (len(colors) - 1))
    return colors[randomColor]
