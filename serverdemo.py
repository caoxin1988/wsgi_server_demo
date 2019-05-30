"""
  Created by Cao,Xin on 2019-05-29 16:38
  Any suggesstions, please send mail to caoxin1988s@gmail.com
"""

# -*- coding: utf-8 -*-

import os
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.utils import redirect
from jinja2 import Environment, FileSystemLoader
from urllib import parse as urlparse


def is_valid_url(url):
    parts = urlparse.urlparse(url)
    return parts.scheme in ('http', 'https')


class ServerDemo(object):

    def __init__(self):
        template_path = os.path.join(os.path.dirname(__file__), 'templates')
        self.jinja_env = Environment(loader=FileSystemLoader(template_path), autoescape=True)
        # get the view func though 'on_' + endpoint
        self.url_map = Map([
            Rule('/', endpoint='new_url')
        ])

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self, 'on_' + endpoint)(request, **values)
        except HTTPException as e:
            return e

    def wsgi_app(self, environ, start_response):
        print('wsgi_app')
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def render_template(self, template_name, **context):
        t = self.jinja_env.get_template(template_name)
        return Response(t.render(context), mimetype='text/html')

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def on_new_url(self, request):
        error = None
        url = ''
        if request.method == "POST":
            url = request.form['url']
            if not is_valid_url(url):
                error = 'please enter a valid URL'
            else:
                return redirect('http://www.baidu.com')

        return self.render_template('new_url.html', error=error, url=url)


def create_app(with_static=True):
    app = ServerDemo()

    if with_static:
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/static' : os.path.join(os.path.dirname(__file__), 'static')
        })

    return app
