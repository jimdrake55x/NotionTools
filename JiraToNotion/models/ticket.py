

class Ticket:

    def __init__(self, id, key, summary, title, labels, created_date, reporter, assignee, subtasks, link):
        self.id = id
        self.key = key
        self.summary = summary
        self.title = title
        self.lables = labels
        self.created_date = created_date
        self.reporter = reporter
        self.assignee = assignee
        self.subtasks = subtasks
        self.link = link
