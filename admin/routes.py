import os
from bottle import route, template, static_file

import admin.api.api_routes
import admin.dashboard.dashboard_routes

# Static files
this_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(this_dir, 'static')
@route('/<path:path>')
def callback(path):
    return static_file(path, static_dir)