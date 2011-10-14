from pyramid.view import view_config


@view_config(route_name='error_list', renderer='triage:templates/error_list.html')
def error_list(request):
	errors = request.db['errors'].find()
	return {'errors': errors}


@view_config(route_name='error_view', renderer='triage:templates/error_view.html')
def error_view(request):
	error_id = request.matchdict['id']
	error = request.db['errors'].find_one({'_id':error_id})
	return { 'error' : error }