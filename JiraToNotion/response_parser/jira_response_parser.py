from jira_builder.jira_builder import make_sprint_requests
from models.sprint import Sprint


def parse_response_to_active_sprints():
    response = make_sprint_requests()

    active_sprints = []
    for sprint in response['values']:
        if sprint['state'] == 'active':
            active_sprints.append(
                Sprint(sprint['name'], sprint['startDate'], sprint['endDate'], []))

    return active_sprints


def parse_response_to_all_sprints():
    response = make_sprint_requests()

    sprints = []
    for sprint in response['values']:

        sprints.append(
            Sprint(sprint['name'], sprint['startDate'], sprint['endDate'], []))

    return sprints
