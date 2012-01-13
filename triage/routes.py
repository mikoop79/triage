def routes(config):
    # Index
    config.add_route('index', '/')
    # Errors
    config.add_route('error_list', '/projects/{project}')
    config.add_route('error_view', '/projects/{project}/error/{id}')
    config.add_route('error_toggle_claim', '/projects/{project}/error/{id}/claim')
    config.add_route('error_toggle_hide', '/projects/{project}/error/{id}/togglehide')
    #Tag
    config.add_route('tag_view', '/projects/{project}/tag/{tag}')
    # REST API
    config.add_route('api_log', 'api/log')
    # Auth
    config.add_route('user_login', 'user/login')
    config.add_route('user_register', 'user/register')
    config.add_route('user_logout', 'user/logout')
