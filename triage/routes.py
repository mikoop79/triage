
def configure_routes(config):
	config.add_route('index', '/')
	config.add_route('jinjatest', '/jinja/{test}')

