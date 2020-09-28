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
