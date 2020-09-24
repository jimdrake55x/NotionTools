from jira.jira_builder import query_active_sprints, query_issues_for_sprint, query_specific_issue
from constants.constants import JIRA_USER_TICKET, JIRA_USER_BASE_REPLACE, JIRA_USER_TICKET_REPLACE, FOLDER_CONFIG_FILE, FOLDER_CONFIG_FILE_REPLACE, FILE_JIRA_CONFIG
from models.jira_config import Jira_Config
from models.sprint import Sprint
from models.ticket import Ticket
from models.user import User
from models.subtask import Subtask
import datetime


def parse_active_sprint_id_response(response):
    response = response['value']
    active_sprints = []

    for sprint in response['active_sprints']:
        active_sprints.append(
            Sprint(sprint['name'], sprint['startDate'], sprint['endDate'], sprint['id'], []))

    return active_sprints


def parse_query_active_sprints_response(response):
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


def parse_query_tickets_for_sprint_response(response):
    issues = response['issues']
    config = Jira_Config()
    tickets = []
    for issue in issues:
        tickets.append(__parse_ticket_from_issue(
            issue, config.jira_cloud_base))

    # This is needed because Jira API does not return Issue-type on top level issues
    # So, when you query a whole sprint, you'll get issues and subtasks at top level, and then
    # Issues will also have their subtasks listed.

    # So here, we go through each issue, and all their subtasks to a list, and then
    # Remove those subtasks from the top level issues.
    subtaskKeys = []
    for ticket in tickets:
        for subtask in ticket.subtasks:
            if subtask.key not in subtaskKeys:
                subtaskKeys.append(subtask.key)

    mainTickets = []
    for ticket in tickets:
        if ticket.key not in subtaskKeys:
            mainTickets.append(ticket)

    return mainTickets


def parse_query_specific_ticket(response):
    issue = response['issues'][0]
    config = Jira_Config()
    return __parse_ticket_from_issue(issue, config.jira_cloud_base)


def __parse_ticket_from_issue(issue, cloudBase):
    # Parse Reporter
    reporter = User(issue['fields']['reporter']['displayName'])

    # Parse Assignee
    assignee = User("Not Assigned")
    try:
        assignee.username = issue['fields']['assignee']['displayName']
    except:
        pass

    # Parse Key
    key = issue['key']

    link = JIRA_USER_TICKET.replace(
        JIRA_USER_BASE_REPLACE, cloudBase)
    link = link.replace(JIRA_USER_TICKET_REPLACE, key)

    # Parse Id
    issueId = issue['id']

    # Parse Summary
    summary = issue['fields']['summary']

    # Parse created At
    createdAt = issue['fields']['created']
    createdAt = datetime.datetime.strptime(createdAt, '%Y-%m-%dT%H:%M:%S.%f%z')

    # Parse Labels
    labels = issue['fields']['labels']

    # Parse Status
    status = issue['fields']['status']['statusCategory']['name']

    # Parse subtasks out
    subtasks = []
    for subtask in issue['fields']['subtasks']:
        subtasks.append(Subtask(subtask['key']))

    ticket = Ticket(issueId, key, summary, key, labels,
                    createdAt, reporter, assignee, subtasks, link, status)

    return ticket
