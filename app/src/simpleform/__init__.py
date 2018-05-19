# -*- coding: utf-8 -*-
from flask import Flask

app = Flask('simpleform')
app.config['SECRET_KEY'] = 'random'
app.debug = True

from .controllers import api_controller