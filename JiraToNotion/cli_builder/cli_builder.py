from __future__ import print_function, unicode_literals
from PyInquirer import prompt, Separator
from pprint import pprint
from jira.jira import get_specific_ticket, get_active_sprint_id, get_tickets_for_sprint
from notion_builder.notion_builder import get_base_page_title, test_insert_page
from sprint_notes_builder.sprint_notes_builder import print_notes
from constants.constants import JTN_VERSION


def get_delivery_options(answers):
    options = ['bike', 'car', 'truck']
    if answers['size'] == 'jumbo':
        options.append('helicopter')
    return options


def print_CLI():
    # General info
    print("=== JTN Version {} ===\n\n".format(JTN_VERSION))

    sprintId = get_active_sprint_id()[0]
    allChoice = 'Import all tickets from \'{0}\''.format(sprintId.name)
    someChoice = 'Import specific tickets from \'{0}\''.format(sprintId.name)
    oneChoice = 'Import a specific ticket...'
    notesChoice = 'Generate Notes For Slack ...'

    questions = [
        {
            'type': 'list',
            'name': 'firstStep',
            'message': 'What would you like to do?',
            'choices': [
                allChoice, someChoice, oneChoice, notesChoice
            ]
        }
    ]

    answer = prompt(questions)
    if answer['firstStep'] == notesChoice:
        questions = [
            {
                'type': 'list',
                'name': 'printStyle',
                'message': 'Which tickets should I print?',
                'choices': [
                    "Print just unfinished tickets...",
                    "Print ALL tickets..."
                ]
            }
        ]
        answer = prompt(questions)
        print_all = answer['printStyle'] == "Print ALL tickets..."
        print_notes(print_all)
    else:
        tickets = get_tickets_for_sprint(sprintId.number)
        if answer['firstStep'] == someChoice:
            ticketKeys = []
            for ticket in tickets:
                ticketKeys.append({'name': ticket.key})

            questions = [
                {
                    'type': 'checkbox',
                    'name': 'tickets',
                    'message': 'Which tickets?',
                    'choices': ticketKeys
                }
            ]
            answer = prompt(questions)
            ticketNames = answer['tickets']
            ticketsToImport = list(
                filter(lambda x: x.key in ticketNames, tickets))
            tickets = ticketsToImport
        elif answer['firstStep'] == oneChoice:
            questions = [
                {
                    'type': 'input',
                    'name': 'ticket_key',
                    'message': 'What is the Ticket Key? (ex. CBUPT-XXXX)'
                }
            ]

            answer = prompt(questions)
            ticketKey = answer['ticket_key']
            ticket = get_specific_ticket(ticketKey)
            tickets = [ticket]

        print("Inserting tickets into notion...")
        test_insert_page(tickets)
        print("Done with tickets...")
