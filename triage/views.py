from pyramid.view import view_config

@view_config(route_name='index', renderer='triage:templates/mytemplate.pt')
def my_view(request):
    return {'project':'triage'}

@view_config(route_name='jinjatest', renderer='jinjatest.jinja2')
def jinjatest(request):
	return {'hello':'world'}

@view_config(route_name='mongo', renderer='mongo.jinja2')
def mongo(request):
	errors = request.db['errors'].find()
	return {'errors':errors}
