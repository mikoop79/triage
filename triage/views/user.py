from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.renderers import render_to_response
from jinja2 import Markup
from triage.forms import UserLoginSchema
from deform import Form, ValidationFailure


@view_config(route_name='user_login')
def login(request):

    schema = UserLoginSchema()
    form = Form(schema, buttons=('submit',))

    if '_id' in request.session:
        return HTTPFound(location='/')

    if 'submit' in request.POST:
        controls = request.POST.items()

        try:
            values = form.validate(controls)

            email = values['email']
            password = values['password']

            user = request.db['users'].find_one({'email': email})

            if not user:
                return HTTPNotFound()

            if (user['password'] == password):
                request.session['_id'] = user['_id']
                return HTTPFound(location='/')

        except ValidationFailure, e:
            form_render = e.render()
    else:
        form_render = form.render()

    params = {
        'form': Markup(form_render)
    }

    return render_to_response('user/register.html', params)


@view_config(route_name='user_logout')
def logout(request):

    if '_id' in request.session:
        del(request.session['_id'])

    return HTTPFound(location='/user/login')
