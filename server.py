"""
  Created by Cao,Xin on 2019-05-29 16:06
  Any suggesstions, please send mail to caoxin1988s@gmail.com
"""

# -*- coding: utf-8 -*-

from serverdemo import ServerDemo, create_app
from werkzeug.serving import run_simple

if __name__ == '__main__':
    app = create_app()
    run_simple('127.0.0.1', 8000, app, use_debugger=True, use_reloader=True)

