from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pymongo.objectid import ObjectId
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import authenticated_userid
from jinja2 import Markup

from triage.models import User, Error, Comment
from triage.forms import CommentsSchema
from deform import Form, ValidationFailure
from time import time



@view_config(route_name='error_list', permission='authenticated')
def list(request):
    available_projects = request.registry.settings['projects']
    selected_project = get_selected_project(request)

    show = request.params.get('show', 'unseen')
    try:
        errors = Error.objects.find_for_list(selected_project, request.user, show)
    except:
        errors = []

    params = {
        'errors': errors,
        'selected_project': selected_project,
        'available_projects': available_projects,
        'show': show,
        'get_error_count': lambda x: Error.objects.find_for_list(selected_project, request.user, x).count()
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

    schema = CommentsSchema()
    form = Form(schema, buttons=('submit',))

    if 'submit' in request.POST:
        controls = request.POST.items()

        try:
            values = form.validate(controls)

            error.comments.append(Comment(
                author = request.user,
                content = values['comment'],
                created = int(time())
            ))
            error.save()

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
        'instance': error.instances[-1],
        'other_errors': error.instances,
        'selected_project': selected_project,
        'available_projects': available_projects,
        'form': Markup(form_render),
    }

    try:
        template = 'error-view/' + str(error['language']).lower() + '.html'
        return render_to_response(template, params)
    except:
        template = 'error-view/generic.html'
        return render_to_response(template, params)


@view_config(route_name='error_toggle_claim', permission='authenticated')
def toggle_claim(request):
    error_id = request.matchdict['id']
    selected_project = get_selected_project(request)

    try:
        error = Error.objects(project=selected_project['id']).with_id(error_id)
        error.claimedby = None if error.claimedby else request.user
        error.save()

        url = request.route_url('error_view', project=selected_project['id'], id=error_id)
        return HTTPFound(location=url)
    except:
        return HTTPNotFound()


@view_config(route_name='error_toggle_hide')
def toggle_hide(request):
    error_id = request.matchdict['id']
    selected_project = get_selected_project(request)

    try:
        error = Error.objects(project=selected_project['id']).with_id(error_id)
        error.hidden = not error.hidden
        error.save()

        url = request.route_url('error_list', project=selected_project['id'])
        return HTTPFound(location=url)
    except:
        return HTTPNotFound()


def get_selected_project(request):
    selected_project_key = request.matchdict['project']
    available_projects = request.registry.settings['projects']

    if selected_project_key in available_projects:
        return available_projects[selected_project_key]
    else:
        raise HTTPNotFound()
