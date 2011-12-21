from pyramid.view import view_config
import base64
import json
from triage.helpers import handle_msg


@view_config(route_name='api_log', renderer='string')
def log(request):
    # Extract error data out of get parameters
    get_params = dict(request.str_GET)

    try:
        error = json.loads(base64.b64decode(get_params['data']))
        handle_msg(error)
    except:
        return {'success': False}

    return {'success': True}
