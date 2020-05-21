from jira_builder.jira_builder import query_active_sprints
from models.sprint import Sprint


def parse_query_active_sprints_response():
    response = query_active_sprints()
    response = response['value']

    active_sprints = []

    for sprint in response['active_sprints']:
        active_sprints.append(
            Sprint(sprint['name'], sprint['startDate'], sprint['endDate'], sprint['id'], []))
    return active_sprints

