from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

import logging
log = logging.getLogger(__name__)


@view_config(route_name='index')
def index(request):
	available_projects = request.registry.settings['projects']
	selected_project = request.registry.settings['default_project']
	url = request.route_url('error_list', project=selected_project)
	return HTTPFound(location=url)
