from jira_builder.jira_builder import query_active_sprints, query_issues_for_sprint, query_specific_issue
from constants.constants import JIRA_USER_TICKET, JIRA_USER_BASE_REPLACE, JIRA_USER_TICKET_REPLACE, FOLDER_CONFIG_FILE, FOLDER_CONFIG_FILE_REPLACE, FILE_JIRA_CONFIG
from models.jira_config import Jira_Config
from models.sprint import Sprint
from models.ticket import Ticket
from models.user import User


def parse_query_active_sprints_response():
    response = query_active_sprints()
    response = response['value']

    active_sprints = []

    for sprint in response['active_sprints']:
        active_sprints.append(
            Sprint(sprint['name'], sprint['startDate'], sprint['endDate'], sprint['id'], []))

    for sprint in active_sprints:
        response = query_issues_for_sprint(sprint.id)
        for ticket in response['issues']:
            name = ticket['key']
            fields = ticket['fields']
            summary = fields['summary']
            sprint.tickets.append(Ticket(name, summary, "", ""))
    return active_sprints

def parse_query_specific_ticket(ticket_name):
    response = query_specific_issue(ticket_name)
    issue = response['issues'][0]

    config = Jira_Config()

    # Ticket Link
    link = JIRA_USER_TICKET.replace(JIRA_USER_BASE_REPLACE, config.jira_cloud_base)
    link = link.replace(JIRA_USER_TICKET_REPLACE, ticket_name)


    # Parse Reporter
    reporter = User(issue['fields']['reporter']['displayName'])
    
    # Parse Assignee
    assignee = User("")
    try:
        assignee.username = issue['fields']['assignee']['displayName']
    except:
        pass

    # Parse Key
    key = issue['key']

    # Parse Id
    issueId = issue['id']

    # Parse Summary
    summary = issue['fields']['summary']

    # Parse created At
    createdAt = issue['fields']['created']

    ticket = Ticket(issueId,key,summary,ticket_name,[],createdAt,reporter,assignee,[], link)

    return ticket
