from pyramid.config import Configurator
import pymongo

from triage.routes import configure_routes
from triage import settings as app_settings

from pyramid_beaker import session_factory_from_settings

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from pyramid.security import Allow, Everyone, Authenticated

import mongoengine


class RootFactory(object):
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, Authenticated, 'authenticated')
    ]

    def __init__(self, request):
        self.request = request


def main(global_config, **settings):
    """ This function returns a WSGI application.
    """

    config = Configurator(settings=settings)
    config.set_session_factory(session_factory_from_settings(settings))

    #authentication/authorization
    config.set_authentication_policy(AuthTktAuthenticationPolicy('seekrit'))
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.set_root_factory(RootFactory)

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

    #mongoengine
    mongoengine.connect(settings['mongodb.db_name'], host=settings['mongodb.host'])

    config.registry.settings['projects'] = app_settings.PROJECTS
    config.registry.settings['default_project'] = app_settings.DEFAULT_PROJECT

    app = config.make_wsgi_app()

    return app
