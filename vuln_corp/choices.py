from vuln_corp.models import User

ISSUE_STATUS = [
    ('New', 'New'),
    ('In Progress', 'In Progress'),
    ('Closed', 'Closed'),
]

ISSUE_ASSIGNEES = [(g.username, g.username) for g in User.query.filter(User.group == 1).all()]
ISSUE_ASSIGNEES.append(('unassigned', 'unassigned'))
print(ISSUE_ASSIGNEES)

CUSTOMERS = [(g.username, g.username) for g in User.query.filter(User.group == 2).all()]
