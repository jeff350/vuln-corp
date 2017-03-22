"""
Utilities for dealing with the UN
"""

import time

from vuln_corp import app
from vuln_corp.models import Issues


def authenticate(scopes):
    pass


@app.template_filter('ctime')
def timectime(s):
    return time.ctime(s)


def get_issue_from_id(id):
    return Issues.query.filter(Issues.id == id).first()
