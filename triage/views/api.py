from pyramid.view import view_config
import base64
import json


@view_config(route_name='api_log', renderer='string')
def log(request):
    available_projects = request.registry.settings['projects']

    get_params = dict(request.str_GET)

    try:
        msg = json.loads(base64.b64decode(get_params['data']))
        error = Error.create_from_msg(msg)
        error.save()
    except:
        return {'success': False}

    return {'success': True}
