"""
  Created by Cao,Xin on 2019-05-29 16:38
  Any suggesstions, please send mail to caoxin1988s@gmail.com
"""

# -*- coding: utf-8 -*-

import os
from werkzeug.wrappers import Request, Response
from werkzeug.wsgi import  SharedDataMiddleware


class ServerDemo(object):

    def __init__(self):
        pass

    def dispatch_request(self, request):
        return Response('hello world!')

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


def create_app(with_static=True):
    app = ServerDemo()

    if with_static:
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/static' : os.path.join(os.path.dirname(__file__), 'static')
        })

    return app
