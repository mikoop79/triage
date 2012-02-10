from pyramid import threadlocal
from pyramid.security import authenticated_userid
from pyramid.events import BeforeRender, ContextFound, subscriber
from triage.models import User
from urllib import urlencode


# Adds route_url method to the top level of the template context
@subscriber(BeforeRender)
def add_route_url(event):
    request = event.get('request') or threadlocal.get_current_request()
    event['route_url'] = request.route_url


# Adds a get_user method to the top level of the template context
@subscriber(BeforeRender)
def add_get_user(event):
    request = event.get('request') or threadlocal.get_current_request()

    try:
        event['user'] = request.user
    except:
        return


# Adds the user to the request after a context is found
@subscriber(ContextFound)
def add_user_to_request(event):
    request = event.request
    userid = authenticated_userid(request)
    if (userid):
        request.user = User.objects().with_id(userid)


# Adds an append_param method to template context to insert values into url GET parameters
@subscriber(BeforeRender)
def add_set_params(event):
    request = event.get('request') or threadlocal.get_current_request()

    def test(params, toggle=False):
        params = params or {}

        for k in request.GET:
            if k not in params:
                params[k] = request.GET[k]
            else:
                if params[k] == request.GET[k] and toggle != False:
                    del(params[k])
                elif k == 'direction':
                    params[k] = 'asc' if request.GET[k] != 'asc' else 'desc'

        return request.current_route_url() + "?" + urlencode(params)
    event['set_params'] = test


@subscriber(BeforeRender)
def add_has_param(event):
    request = event.get('request') or threadlocal.get_current_request()

    def test(params):
        value = 'inactive'
        params = params or {}
        for k in request.GET:
            if k in params and params[k] == request.GET[k]:
                value = 'active'
        return value

    event['has_param'] = test
