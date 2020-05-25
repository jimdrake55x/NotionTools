from jira_builder.jira_builder import query_active_sprints, query_issues_for_sprint
from models.sprint import Sprint
from models.ticket import Ticket


def parse_query_active_sprints_response():
    response = query_active_sprints()
    response = response['value']

    active_sprints = []

    for sprint in response['active_sprints']:
        active_sprints.append(
            Sprint(sprint['name'], sprint['startDate'], sprint['endDate'], sprint['id'], []))

    for sprint in active_sprints:
        tickets = []
        response = query_issues_for_sprint(sprint.id)
        for ticket in response['issues']:
            name = ticket['key']
            fields = ticket['fields']
            summary = fields['summary']

            sprint.tickets.append(Ticket(name, summary, "", ""))
    return active_sprints
