from pyramid.view import view_config
from pyramid.renderers import render_to_response, get_renderer
from pymongo.objectid import ObjectId
from triage.helpers import get_errors
from pymongo import DESCENDING


@view_config(route_name='error_list')
def error_list(request):
	errors = get_errors(request, 'contest-errors')
	params = {'errors': errors}
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
