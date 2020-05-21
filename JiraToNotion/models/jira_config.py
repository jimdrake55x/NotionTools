
class Jira_Config():

    def __init__(self, jira_data):
        self.username = jira_data['username']
        self.token = jira_data['token']
        self.board_number = jira_data['board_number']
        self.jira_cloud_base = jira_data['jira_cloud_base']
