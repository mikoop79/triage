from pyramid.view import view_config


@view_config(route_name='index', renderer='triage:templates/main.html')
def my_view(request):
	errors = request.db['errors'].find()
	return {'errors': errors}
