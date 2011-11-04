
def configure_routes(config):
	config.add_route('index', '/')
	config.add_route('error_list', '/projects/{project}')
	config.add_route('error_view', 'error/{id}')
	config.add_route('error_hide', 'error/{id}/hide')
	config.add_route('error_show', 'error/{id}/show')
	config.add_route('api_log', 'api/log')