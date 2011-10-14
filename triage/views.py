from pyramid.view import view_config
from pymongo.objectid import ObjectId
from triage.helpers import get_errors

@view_config(route_name='error_list', renderer='triage:templates/error_list.html')
def error_list(request):

	errors = get_errors(request, 'contest-errors')
	return {'errors': errors}


@view_config(route_name='error_view', renderer='triage:templates/error_view.html')
def error_view(request):
	error_id = request.matchdict['id']
	error = request.db['contest-errors'].find_one({'_id':ObjectId(error_id)})

	other_errors = request.db['contest-errors'].find({ 'type': error['type'], 'line': error['line'], 'file': error['file'] })

	return { 'error' : error , 'other_errors': other_errors }