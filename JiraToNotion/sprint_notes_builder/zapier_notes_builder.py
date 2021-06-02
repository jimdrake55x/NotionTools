import json
import requests
from requests.auth import HTTPBasicAuth
import datetime

# DELETE COMMENT
# This script works in Zapier to produce Tickets for use in other actions. 
# Step 1: Fill in constants below with your information
# Step 2: Copy and paste this whole file into a `Code By Zapier` python action step.
# Step 3: Use results to post whatever you want 👍
# Step 4: Delete this comment

# Constants - Fill these in yourself
JIRA_API_EVAL_URL = 'https://{FILL IN}.atlassian.net/rest/api/3/expression/eval'
JIRA_API_JQL_URL = 'https://{FILL IN}.atlassian.net/rest/api/3/search'
TOKEN = '{FILL IN}'
USERNAME = '{FILL IN}'
BOARD_NUMBER =  '{FILL IN}'
JIRA_SORT_ID = "{FILL IN}"
JIRA_CLOUD_BASE = "{FILL IN}"
JIRA_USER_TICKET = 'https://{br}.atlassian.net/browse/{t}'
JIRA_USER_BASE_REPLACE = '{br}'
JIRA_USER_TICKET_REPLACE = '{t}'


# Classes
class Ticket:
    def __init__(self, id, key, summary, title, labels, created_date, reporter, assignee, subtasks, link, status, ticket_type):
        self.id = id
        self.key = key
        self.summary = summary
        self.title = title
        self.labels = labels
        self.created_date = created_date
        self.reporter = reporter
        self.assignee = assignee
        self.subtasks = subtasks
        self.link = link
        self.status = status
        self.ticket_type = ticket_type

class User:
    def __init__(self, username):
        self.username = username

class Status:
    def __init__(self, status, color):
        self.status = status
        self.color = color


class Subtask:
    def __init__(self, key):
        self.key = key


class Sprint:
    def __init__(self, name, start_date, end_date, number, tickets=[]):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.number = number
        self.tickets = tickets

# End of Classes

# Making Requests
def __make_jira_query_request(query):
    api = JIRA_API_EVAL_URL

    auth = HTTPBasicAuth(USERNAME, TOKEN)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = query

    try:
        response = requests.request(
            "POST",
            api,
            data=payload,
            headers=headers,
            auth=auth
        )

    except Exception as e:
        print('Something went wrong with requesting sprint information. Is your board # correct?')
        print(e)

    return json.loads(response.text)


def __make_jira_jql_request(jql):
    api = JIRA_API_JQL_URL

    auth = HTTPBasicAuth(USERNAME, TOKEN)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = jql

    try:
        response = requests.request(
            "POST",
            api,
            data=payload,
            headers=headers,
            auth=auth
        )

    except Exception as e:
        print('Something went wrong with requesting sprint information. Is your board # correct?')
        print(e)

    return json.loads(response.text)

def query_active_sprints():
    query = json.dumps({
        "expression": "{active_sprints: board.activeSprints}",
        "context": {
            "board": BOARD_NUMBER
        }
    })

    return __make_jira_query_request(query)

def query_issues_for_sprint_ordered(sprintNumber, orderByProperty):
    jql_sprint = "sprint = " + str(sprintNumber) + " order by cf[" + str(orderByProperty) +"]"
    jql = json.dumps({
        "jql": jql_sprint,
        "fields": [
            "summary",
            "created",
            "assignee",
            "reporter",
            "subtasks",
            "labels",
            "status",
            "issuetype"
        ],
        "maxResults": 150
    })

    return __make_jira_jql_request(jql)
# End of making requests

# Parsing request results
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
    status = Status(issue['fields']['status']['statusCategory']['name'],
                    issue['fields']['status']['statusCategory']['colorName'])

    # Parse subtasks out
    subtasks = []
    for subtask in issue['fields']['subtasks']:
        subtasks.append(Subtask(subtask['key']))

    # Parse type
    ticket_type = issue['fields']['issuetype']['name']

    ticket = Ticket(issueId, key, summary, key, labels,
                    createdAt, reporter, assignee, subtasks, link, status, ticket_type)

    return ticket

def parse_query_tickets_for_sprint_response(response):
    issues = response['issues']
    tickets = []
    for issue in issues:
        tickets.append(__parse_ticket_from_issue(
            issue, JIRA_CLOUD_BASE))

    mainTickets = list(filter(lambda x: x.ticket_type not in [
                       "Sub-Task", "Sub-Defect", "Goal", "Impediment"], tickets))
    return mainTickets

def parse_active_sprint_id_response(response):
    response = response['value']
    active_sprints = []

    for sprint in response['active_sprints']:
        active_sprints.append(
            Sprint(sprint['name'], sprint['startDate'], sprint['endDate'], sprint['id'], []))

    return active_sprints
# End of parsing results from requests

# Helper methods
def get_active_sprint_id():
    apiResponse = query_active_sprints()
    sprintId = parse_active_sprint_id_response(apiResponse)
    return sprintId

def get_tickets_for_sprint(sprintNumber):
    api_response = query_issues_for_sprint_ordered(sprintNumber, JIRA_SORT_ID)
    tickets = parse_query_tickets_for_sprint_response(api_response)
    return tickets
# End of Helpers

def print_notes(print_all_tickets):
    json_response = []

    tickets = get_tickets_for_sprint(get_active_sprint_id()[0].number)

    if not print_all_tickets:
        tickets = list(filter(lambda x: x.status.status != "Done", tickets))

    for ticket in tickets:
        stringToPrint = "*{0}*: {1}".format(ticket.title, ticket.summary)
        json_response.append({'Ticket':stringToPrint})
        
    return json_response

output = print_notes(False)
