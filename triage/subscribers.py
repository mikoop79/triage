from pyramid import threadlocal
from pyramid.security import authenticated_userid
from pyramid.events import BeforeRender, ContextFound, subscriber
from triage.models import User


# Adds route_url method to the top level of the template context
@subscriber(BeforeRender)
def add_route_url(event):
    request = event.get('request') or threadlocal.get_current_request()
    event['route_url'] = request.route_url


# Adds a get_user method to the top level of the template context
@subscriber(BeforeRender)
def add_get_user(event):
    request = event.get('request') or threadlocal.get_current_request()
    userid = authenticated_userid(request)

    try:
        event['get_user'] = User.objects().with_id(userid)
    except:
        return


# Adds the user to the request after a context is found
@subscriber(ContextFound)
def add_user_to_request(event):
	request = event.request
	userid = authenticated_userid(request)
	if (userid):
		request.user = User.objects().with_id(userid)
