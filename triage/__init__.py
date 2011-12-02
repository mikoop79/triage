from pyramid.config import Configurator
import pymongo

from triage.routes import configure_routes
from triage import settings as app_settings

from pyramid_beaker import session_factory_from_settings


def main(global_config, **settings):
    """ This function returns a WSGI application.
    """

    session_factory = session_factory_from_settings(settings)
    config = Configurator(settings=settings)
    config.set_session_factory(session_factory)

    #beaker
    config.include('pyramid_beaker')
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

    app = config.make_wsgi_app()

    return app
