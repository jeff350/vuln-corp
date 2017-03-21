"""
Utilities for dealing with the UN
"""

import time

from vuln_corp import app


def authenticate(scopes):
    pass


@app.template_filter('ctime')
def timectime(s):
    return time.ctime(s)
