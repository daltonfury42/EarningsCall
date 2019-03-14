#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/EarningsCall/")

from backend import app as application
application.secret_key = 'Add your secret key'
