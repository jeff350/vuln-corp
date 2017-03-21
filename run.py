#!/usr/bin/env python
from werkzeug.serving import run_simple

import config
from vuln_corp import app

if config.DEBUG_MODE:
    app.run(host='0.0.0.0', debug=True)
else:
    from werkzeug.debug import DebuggedApplication

    app2 = DebuggedApplication(app, evalex=True, pin_security=False)
    run_simple('0.0.0.0', 5000, app2, use_debugger=True)
