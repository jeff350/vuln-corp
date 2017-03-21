#!/usr/bin/env python
from vuln_corp import db, models

# roles 1-Admin 2-Customer
db.session.add(models.Groups('Admin'))
db.session.add(models.Groups('customer'))

db.session.add(models.User('admin', 'Jeff', 'Neel', 'admin@mil.gov', 'pw', 1, 'About admin'))
db.session.add(models.User('customer', 'Jeff', 'Neel', 'customer@iastate.edu', 'pw', 2, 'About customer'))
db.session.commit()
