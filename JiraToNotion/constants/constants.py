# Jira API
JIRA_API_EVAL_URL = 'https://{br}.atlassian.net/rest/api/3/expression/eval'
JIRA_API_BASE_REPLACE = '{br}'
JIRA_API_JQL_URL = 'https://{br}.atlassian.net/rest/api/3/search'

# Jira User Facing
JIRA_USER_TICKET = 'https://{br}.atlassian.net/browse/{t}'
JIRA_USER_BASE_REPLACE = '{br}'
JIRA_USER_TICKET_REPLACE = '{t}'


# Folder Path Constants
FOLDER_DATA = './JiraToNotion/data/'
FOLDER_DATA_FILE_REPLACE = '{f}'
FOLDER_DATA_FILE = FOLDER_DATA + FOLDER_DATA_FILE_REPLACE

FOLDER_CONFIG = './JiraToNotion/configs/'
FOLDER_CONFIG_FILE_REPLACE = '{cf}'
FOLDER_CONFIG_FILE = FOLDER_CONFIG + FOLDER_CONFIG_FILE_REPLACE

# File Constants
FILE_SPRINT_DATA = 'data_sprint.json'
FILE_TICKETS_DATA = 'data_tickets.json'
FILE_TICKET_DATA = 'data_ticket.json'
FILE_JIRA_CONFIG = 'jira_config.json'
FILE_NOTION_CONFIG = 'notion_config.json'
