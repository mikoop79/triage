
def configure_routes(config):
	config.add_route('error_list', '/{project:.*}')	
	config.add_route('error_view', 'error/{id}')
