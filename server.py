# server.py
# Math tools web application
# Author: Sébastien Combéfis
# Version: February 3, 2016

import os
from bottle import route, run

@route('/')
def home():
    return 'Hello World!'

run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))