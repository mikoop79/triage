import pyramid.threadlocal as threadlocal
from pyramid.events import BeforeRender, subscriber


@subscriber(BeforeRender)
def add_route_url(event):
	request = event.get('request') or threadlocal.get_current_request()
	if not request:
		return
	event['route_url'] = request.route_url