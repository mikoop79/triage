from pyramid.view import view_config

@view_config(route_name='index', context='triage:resources.Root',  renderer='triage:templates/mytemplate.pt')
def my_view(request):
    return {'project':'triage'}

@view_config(route_name='jinjatest', context='triage:resources.Root', renderer='jinjatest.jinja2')
def jinjatest(request):
	return {'hello':'world'}
