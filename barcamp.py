# coding: utf-8

"""
    Application and settings
"""

from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.routing import Rule

import redis

app = None

class GeneratorRule(Rule):
    def __init__(self, rule, **kwargs):
        self.generator = kwargs.get('generator', None)
        if self.generator:
            kwargs.pop('generator')

        super(GeneratorRule, self).__init__(rule, **kwargs)

def create_app(config):
    global app
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.config.update(config)

    app.url_rule_class = GeneratorRule

    app.redis = redis.Redis()

    import views
    import login
    import login_oauth
    import talks
    import program
    import entrant
    import vote
    import filters
    import presenters_go
    import service
    return app
