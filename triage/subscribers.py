from pyramid import threadlocal
from pyramid.security import authenticated_userid
from pyramid.events import BeforeRender, ContextFound, subscriber
from triage.models import User
from urllib import urlencode
from webob.multidict import MultiDict
from datetime import datetime, timedelta

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
def add_toggle_params(event):
    request = event.get('request') or threadlocal.get_current_request()

    def test(**kwargs):
        key = kwargs.keys()[0]
        value = str(kwargs.values()[0])
        params = request.GET.copy()

        if value in params.getall(key):
            vals = list(params.getall(key))
            del params[key]
            for v in vals:
                if value != v:
                    params.add(key, v)
        else:
            params.add(key, value)

        return request.current_route_url() + "?" + urlencode(params)
    event['toggle_param'] = test


# Adds an append_param method to template context to insert values into url GET parameters
@subscriber(BeforeRender)
def add_set_params(event):
    request = event.get('request') or threadlocal.get_current_request()

    def test(params, toggle=False, multi=False):
        params = MultiDict(params or {})

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
def add_date(event):
    def test(timestamp, format_today='%I:%M %p', format_other='%d %b %y'):

        today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow = today + timedelta(days=1)
        date = datetime.fromtimestamp(timestamp)
        
        if date >= today and date < tomorrow:
            return date.strftime(format_today)
        
        return date.strftime(format_other)

    event['date'] = test


@subscriber(BeforeRender)
def add_switch(event):
    def test(condition, true='active', false='inactive'):
        if condition:
            return true
        return false

    event['switch'] = test


@subscriber(BeforeRender)
def add_has_param(event):
    request = event.get('request') or threadlocal.get_current_request()

    def test(**kwargs):
        key = kwargs.keys()[0]
        value = str(kwargs.values()[0])
        return value in request.GET.getall(key)

    event['has_param'] = test
