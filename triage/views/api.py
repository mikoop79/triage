from pyramid.view import view_config
import base64
import json
from triage.models import Error

@view_config(route_name='api_log', renderer='string')
def log(request):
    available_projects = request.registry.settings['projects']

    get_params = dict(request.str_GET)
    try:
        msg = json.loads(base64.b64decode(get_params['data']))
        msg = _format_backtrace(msg)

        error = Error.create_from_msg(msg)
        error.save()
    except:
        return {'success': False}

    return {'success': True}


def _format_backtrace(msg):
    if ('backtrace' in msg):
        backtrace = []
        for trace in msg['backtrace']:
            backtrace.append({
                'class': '',
                'file': '',
                'function': trace,
                'line': 'n/a'
            })
        msg['backtrace'] = backtrace
    return msg
