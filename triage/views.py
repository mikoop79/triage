from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pymongo.objectid import ObjectId
from triage.helpers import get_errors
from pymongo import DESCENDING

@view_config(route_name='error_list')
def error_list(request):
	selected_project_key = request.matchdict['project']
	available_projects = request.registry.settings['projects']

	if selected_project_key in available_projects:
		selected_project = available_projects[selected_project_key]
	else:
		selected_project = next(available_projects.itervalues()) #pick a default

	print selected_project
	errors = get_errors(request, selected_project)
	params = { 
		'errors': errors,
		'selected_project': selected_project,
		'available_projects': available_projects
	}
	return render_to_response('error-list.html', params)


@view_config(route_name='error_view')
def error_view(request):
	error_id = request.matchdict['id']
	error = request.db['contest-errors'].find_one({'_id': ObjectId(error_id)})

	other_errors = request.db['contest-errors'].find({
		'type': error['type'],
		'line': error['line'],
		'file': error['file']
	}).sort('timestamp', DESCENDING)

	params = {'error': error, 'other_errors': other_errors}

	try:
		template = 'error-view/'+str(error['language']).lower()+'.html'
		return render_to_response(template, params)
	except:
		template = 'error-view/generic.html'
		return render_to_response(template, params)
