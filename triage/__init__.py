from pyramid.config import Configurator
from pyramid.events import subscriber
from pyramid.events import NewRequest
import pymongo

from triage.resources import Root
from triage.routes import configure_routes
from triage import settings as app_settings

def main(global_config, **settings):
    """ This function returns a WSGI application.
    """
    config = Configurator(settings=settings, root_factory=Root)
    #jinja2
    config.include('pyramid_jinja2')
    config.add_renderer('.html', 'pyramid_jinja2.renderer_factory')
    #views
    config.add_static_view('static', 'triage:static')
    config.scan('triage.views')
    #routes
    configure_routes(config)
    # MongoDB
    def add_mongo_db(event):
        settings = event.request.registry.settings
        url = settings['mongodb.url']
        db_name = settings['mongodb.db_name']
        db = settings['mongodb_conn'][db_name]
        event.request.db = db
    db_uri = settings['mongodb.url']
    conn = pymongo.Connection(db_uri)
    config.registry.settings['mongodb_conn'] = conn
    config.registry.settings['projects'] = app_settings.PROJECTS
    config.registry.settings['default_project'] = app_settings.DEFAULT_PROJECT
    config.add_subscriber(add_mongo_db, NewRequest)
    return config.make_wsgi_app()
