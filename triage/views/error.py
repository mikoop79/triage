from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pymongo.objectid import ObjectId
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import authenticated_userid
from pymongo import DESCENDING
from jinja2 import Markup

from triage.models import User, Error
from triage.forms import CommentsSchema
from deform import Form, ValidationFailure
from time import time


def get_error_count(request, selected_project, show):
    return get_filter(selected_project, show).count()


def get_filter(selected_project, show):
    if show == 'all':
        return Error.objects(project=selected_project)
    elif show == 'hidden':
        return Error.objects(project=selected_project, hidden=True)
    elif show == 'seen':
        return Error.objects(project=selected_project, seen=True, hidden__ne=True)
    elif show == 'unseen':
        return Error.objects(project=selected_project, seen__ne=True, hidden__ne=True)


@view_config(route_name='error_list', permission='authenticated')
def list(request):
    available_projects = request.registry.settings['projects']
    selected_project = get_selected_project(request)

    show = request.params.get('show', 'unseen')

    try:
        errors = Error.objects(project=selected_project['id'])
    except:
        errors = []

    params = {
        'errors': errors,
        'selected_project': selected_project,
        'available_projects': available_projects,
        'show': show,
        'get_error_count': lambda x: get_error_count(request, selected_project['id'], x)
    }

    return render_to_response('error-list.html', params)


@view_config(route_name='error_view', permission='authenticated')
def view(request):
    available_projects = request.registry.settings['projects']
    selected_project = get_selected_project(request)

    error_id = request.matchdict['id']
    try:
        error = Error.objects(project=selected_project['id']).with_id(error_id)
    except:
        return HTTPNotFound()

    user = User.objects().with_id(authenticated_userid(request))

    schema = CommentsSchema()
    form = Form(schema, buttons=('submit',))

    if 'submit' in request.POST:
        controls = request.POST.items()

        try:
            values = form.validate(controls)

            comments = error.get('comments', [])
            comments.append({
                'name': user['email'],
                'comment': values['comment'],
                'timecreated': int(time())
            })
            error['comments'] = comments

            request.db[selected_project['collection']].save(error)

            url = request.route_url('error_view', project=selected_project['id'], id=error_id)
            return HTTPFound(location=url)
        except ValidationFailure, e:
            form_render = e.render()
    else:
        form_render = form.render()

    error.seen = True
    error.save()

    params = {
        'error': error,
        'other_errors': error.instances,
        'selected_project': selected_project,
        'available_projects': available_projects,
        'form': Markup(form_render),
        'user': user
    }

    try:
        template = 'error-view/' + str(error['language']).lower() + '.html'
        return render_to_response(template, params)
    except:
        template = 'error-view/generic.html'
        return render_to_response(template, params)


@view_config(route_name='error_toggle_claim', permission='authenticated')
def toggle_claim(request):
    selected_project = get_selected_project(request)

    error_id = request.matchdict['id']
    error = request.db[selected_project['collection']].find_one({'_id': ObjectId(error_id)})
    user = User.get_by_userid(request, authenticated_userid(request))

    if error and user:
        error['claimed'] = None if error.get('claimed') else user['_id']
        request.db[selected_project['collection']].save(error)

        url = request.route_url('error_view', project=selected_project['id'], id=error_id)
        return HTTPFound(location=url)

    return HTTPNotFound()


@view_config(route_name='error_toggle_hide')
def toggle_hide(request):
    selected_project = get_selected_project(request)

    error_id = request.matchdict['id']
    error = request.db[selected_project['collection']].find_one({'_id': ObjectId(error_id)})

    if error:
        error['hidden'] = not error.get('hidden', False)
        request.db[selected_project['collection']].save(error)

        url = request.route_url('error_list', project=selected_project['id'])
        return HTTPFound(location=url)

    return HTTPNotFound()


def get_selected_project(request):
    selected_project_key = request.matchdict['project']
    available_projects = request.registry.settings['projects']

    if selected_project_key in available_projects:
        return available_projects[selected_project_key]
    else:
        raise HTTPNotFound()
