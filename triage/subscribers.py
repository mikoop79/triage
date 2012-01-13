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
def add_param_adder(event):
    request = event.get('request') or threadlocal.get_current_request()
    def test(params):
        params = params or {}
        for k in request.GET:
            if k not in params:
                params[k] = request.GET[k]
        return request.current_route_url() + "?" + urlencode(params)
    event['append_param'] = test

# Adds a remove_param method to template context to remove values from GET parameters
@subscriber(BeforeRender)
def add_param_remove(event):
    request = event.get('request') or threadlocal.get_current_request()
    def test(params):
        params = params or {}
        for k in params:
            if k in request.GET:
                del request.GET[k]
        return request.current_route_url() + "?" + urlencode(params)
    event['remove_param'] = test