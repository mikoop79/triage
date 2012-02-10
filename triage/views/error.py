from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from jinja2 import Markup

from triage.util import Paginator
from triage.models import Error, Comment, Tag
from triage.forms import CommentsSchema, TagSchema
from deform import Form, ValidationFailure
from time import time


@view_config(route_name='error_list', permission='authenticated')
def list(request):
    available_projects = request.registry.settings['projects']
    selected_project = get_selected_project(request)

    show = request.params.get('show', 'all')
    try:
        errors = Error.objects.find_for_list(selected_project, request.user, show)
    except:
        errors = []

    tag = request.params.get('tag', False)
    if tag != False and errors.count():
        errors.filter(tags=tag)

    order_by = request.params.get('order', False)
    direction = request.params.get('direction', False)
    if order_by != False and errors.count():
        if direction and direction == 'desc':
            order_by = '-' + order_by
        errors.order_by(order_by)

    page = request.params.get('page', '1')
    paginator = Paginator(errors, size_per_page=20, current_page=page)

    params = {
        'errors': paginator.get_current_page(),
        'paginator': paginator,
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

    comment_schema = CommentsSchema()
    comment_form = Form(comment_schema, buttons=('submit',), formid="comment_form")

    tag_schema = TagSchema()
    tag_form = Form(tag_schema, buttons=('submit',), formid="tag_form")

    if 'submit' in request.POST:
        form_id = request.POST['__formid__']
        controls = request.POST.items()

        if form_id == 'comment_form':
            try:
                values = comment_form.validate(controls)

                error.comments.append(Comment(
                    author=request.user,
                    content=values['comment'],
                    created=int(time())
                ))
                error.save()

                url = request.route_url('error_view', project=selected_project['id'], id=error_id)
                return HTTPFound(location=url)
            except ValidationFailure, e:
                comment_form_render = e.render()
        elif form_id == 'tag_form':
            try:
                values = tag_form.validate(controls)

                # build a list of comma seperated, non empty tags
                tags = [t.strip() for t in values['tag'].split(',') if t.strip() != '']

                for tag in tags:
                    if tag not in error.tags:
                        error.tags.append(tag)
                        error.save()

                        tag = Tag.create(tag)
                        tag.save()

                url = request.route_url('error_view', project=selected_project['id'], id=error_id)
                return HTTPFound(location=url)
            except ValidationFailure, e:
                tag_form_render = e.render()
    else:
        comment_form_render = comment_form.render()
        tag_form_render = tag_form.render()

    error.seen = True
    error.save()

    params = {
        'error': error,
        'instance': error.instances[-1],
        'other_errors': error.instances,
        'selected_project': selected_project,
        'available_projects': available_projects,
        'comment_form': Markup(comment_form_render),
        'tag_form': Markup(tag_form_render),
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
