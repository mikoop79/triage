from pyramid.view import view_config
from pymongo.objectid import ObjectId
from triage.helpers import get_errors
from pymongo import DESCENDING

@view_config(route_name='error_list', renderer='triage:templates/error_list.html')
def error_list(request):
	selected_project_key = request.matchdict['project']
	available_projects = request.registry.settings['projects']

	if selected_project_key in available_projects:
		selected_project = available_projects[selected_project_key]
	else:
		selected_project = next(available_projects.itervalues()) #pick a default

	print selected_project
	errors = get_errors(request, selected_project)
	return { 
		'errors': errors,
		'selected_project': selected_project,
		'available_projects': available_projects
	}


@view_config(route_name='error_view', renderer='triage:templates/error_view.html')
def error_view(request):
	error_id = request.matchdict['id']
	error = request.db['contest-errors'].find_one({'_id':ObjectId(error_id)})

	other_errors = request.db['contest-errors'].find({ 
		'type': error['type'],
		'line': error['line'],
		'file': error['file'] 
	}).sort('timestamp', DESCENDING)

	return { 'error' : error , 'other_errors': other_errors }