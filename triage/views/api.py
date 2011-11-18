from pyramid.view import view_config
from time import time
import base64, json
import pprint #Use for dumping objects pprint.pprint(object)


@view_config(route_name='api_log', renderer='string')
def log(request):
	available_projects = request.registry.settings['projects']

	# Extract error data out of get parameters
	get_params = dict(request.str_GET)
	error = json.loads( base64.b64decode(get_params['data']) )
	error["timestamp"] = time.time()

	try:
		selected_project = available_projects[error['application']]
		request.db[selected_project['collection']].insert(error)
	except:
		return { 'success' : False }

	return { 'success' : True }
