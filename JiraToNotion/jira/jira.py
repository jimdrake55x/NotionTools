from models.jira_config import Jira_Config
from jira.jira_builder import query_issues_for_sprint, query_specific_issue, query_active_sprints, query_issues_for_sprint_ordered
from jira.jira_response_parser import parse_query_specific_ticket, parse_active_sprint_id_response, parse_query_tickets_for_sprint_response

from models.sprint import Sprint


def get_specific_ticket(ticketName):
    apiResponse = query_specific_issue(ticketName)
    ticket = parse_query_specific_ticket(apiResponse)
    return ticket


def get_active_sprint_id():
    apiResponse = query_active_sprints()
    sprintId = parse_active_sprint_id_response(apiResponse)
    return sprintId


def get_tickets_for_sprint(sprintNumber):
    jira_config = Jira_Config();
    if jira_config.jira_sort_property_id:
        apiResponse = query_issues_for_sprint_ordered(sprintNumber,jira_config.jira_sort_property_id)
    else:
        apiResponse = query_issues_for_sprint(sprintNumber)
    tickets = parse_query_tickets_for_sprint_response(apiResponse)
    return tickets
