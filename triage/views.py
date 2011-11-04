from time import time
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pymongo.objectid import ObjectId
from triage.helpers import get_errors, get_error_count
from pymongo import DESCENDING
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
import time

import logging
log = logging.getLogger(__name__)

import pyramid.threadlocal as threadlocal
from pyramid.events import BeforeRender, subscriber
@subscriber(BeforeRender)
def add_route_url(event):
    request = event.get('request') or threadlocal.get_current_request()
    if not request:
        return
    event['route_url'] = request.route_url



@view_config(route_name='index')
def index(request):
	available_projects = request.registry.settings['projects']
	selected_project = request.registry.settings['default_project']
	url = request.route_url('error_list', project=selected_project) 
	return HTTPFound(location=url)



@view_config(route_name='error_list')
def error_list(request):
	available_projects = request.registry.settings['projects']
	selected_project = get_selected_project(request)

	show = request.params.get('show', 'unseen')

	try:
		errors = get_errors(request, selected_project, show)
	except:
		errors = []
		
	params = { 
		'errors': errors,
		'selected_project': selected_project,
		'available_projects': available_projects,
		'show': show,
		'get_error_count': lambda x: get_error_count(request, selected_project, x)
	}

	return render_to_response('error-list.html', params)



@view_config(route_name='error_view')
def error_view(request):
	available_projects = request.registry.settings['projects']
	selected_project = get_selected_project(request)

	error_id = request.matchdict['id']
	error = request.db[selected_project['collection']].find_one({'_id': ObjectId(error_id)})

	if not error:
		return HTTPNotFound()

	error['seen'] = True
	request.db[selected_project['collection']].save(error)

	other_errors = request.db['contest-errors'].find({
		'type': error.get('type', None),
		'line': error.get('line', None),
		'file': error.get('file', None)
	}).sort('timestamp', DESCENDING)

	params = {
		'error': error,
		'other_errors': other_errors,
		'selected_project': selected_project,
		'available_projects': available_projects		
	}

	try:
		template = 'error-view/'+str(error['language']).lower()+'.html'
		return render_to_response(template, params)
	except:
		template = 'error-view/generic.html'
		return render_to_response(template, params)



@view_config(route_name='error_hide')
def error_hide(request):
	available_projects = request.registry.settings['projects']
	selected_project = get_selected_project(request)

	error_id = request.matchdict['id']
	error = request.db[selected_project['collection']].find_one({'_id': ObjectId(error_id)})

	if error != None:
		error['hidden'] = True
		request.db[selected_project['collection']].save(error)
		
		url = request.route_url('error_list', project=selected_project['id']) 
		return HTTPFound(location=url)

	return HTTPNotFound()
	
	return { 'error' : error , 'other_errors': other_errors }



@view_config(route_name='error_show')
def error_show(request):
	available_projects = request.registry.settings['projects']
	selected_project = get_selected_project(request)
		
	error_id = request.matchdict['id']
	error = request.db[selected_project['collection']].find_one({'_id': ObjectId(error_id)})

	if error != None:
		error['hidden'] = False
		request.db[selected_project['collection']].save(error)
		
		url = request.route_url('error_list', project=selected_project['id']) 
		return HTTPFound(location=url)

	return HTTPNotFound()
	
	return { 'error' : error , 'other_errors': other_errors }



@view_config(route_name='api_log', renderer='string')
def api_log(request):
	available_projects = request.registry.settings['projects']

	error = dict(request.str_GET)
	error["timestamp"] = time.time()

	try:
		selected_project = available_projects[error['application']]	
		request.db[selected_project['collection']].insert(error)
	except:
		return { 'success' : False }

	return { 'success' : True }



def get_selected_project(request):
	selected_project_key = request.matchdict['project']
	available_projects = request.registry.settings['projects']

	if selected_project_key in available_projects:
		return available_projects[selected_project_key]
	else:
		raise HTTPNotFound()

