from pyramid.config import Configurator
import pymongo

from triage.routes import configure_routes
from triage import settings as app_settings


def main(global_config, **settings):
    """ This function returns a WSGI application.
    """
    config = Configurator(settings=settings)
    #jinja2
    config.include('pyramid_jinja2')
    config.add_renderer('.html', 'pyramid_jinja2.renderer_factory')
    #views
    config.add_static_view('static', 'triage:static')
    config.scan('triage.views')
    config.scan('triage.subscribers')
    #routes
    configure_routes(config)
    # MongoDB
    db_uri = settings['mongodb.url']
    conn = pymongo.Connection(db_uri)
    config.registry.settings['mongodb_conn'] = conn
    config.registry.settings['projects'] = app_settings.PROJECTS
    config.registry.settings['default_project'] = app_settings.DEFAULT_PROJECT
    return config.make_wsgi_app()


