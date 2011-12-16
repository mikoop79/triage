

def configure_routes(config):
    config.add_route('index', '/')
    config.add_route('error_list', '/projects/{project}')
    config.add_route('error_view', '/projects/{project}/error/{id}')
    config.add_route('error_toggle_claim', '/projects/{project}/error/{id}/claim')
    config.add_route('error_toggle_hide', '/projects/{project}/error/{id}/togglehide')
    config.add_route('api_log', 'api/log')
    config.add_route('user_login', 'user/login')
    config.add_route('user_register', 'user/register')
    config.add_route('user_logout', 'user/logout')
