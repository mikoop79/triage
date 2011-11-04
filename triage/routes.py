
def configure_routes(config):
	config.add_route('index', '/')
	config.add_route('error_list', '/projects/{project}')
	config.add_route('error_view', '/projects/{project}/error/{id}')
	config.add_route('error_hide', '/projects/{project}/error/{id}/hide')
	config.add_route('error_show', '/projects/{project}/error/{id}/show')
	config.add_route('api_log', 'api/log')