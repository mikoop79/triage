from pyramid.view import view_config


@view_config(route_name='error_list', renderer='triage:templates/error_list.html')
def error_list(request):
	errors = request.db['errors'].find()
	return {'errors': errors}
