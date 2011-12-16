from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.renderers import render_to_response
from jinja2 import Markup
from triage.forms import UserLoginSchema, UserRegisterSchema, user_register_validator, user_login_validator
from deform import Form, ValidationFailure
from pyramid.security import remember, forget
from pyramid.security import authenticated_userid
from triage.models import User
from time import time
from mongoengine.queryset import DoesNotExist


@view_config(route_name='user_login')
@view_config(context='pyramid.httpexceptions.HTTPForbidden')
def login(request):

    schema = UserLoginSchema(validator=user_login_validator)
    form = Form(schema, buttons=('submit',))

    userid = authenticated_userid(request)
    if userid:
        return HTTPFound(location='/')

    if 'submit' in request.POST:
        controls = request.POST.items()

        try:
            values = form.validate(controls)

            try:
                user = User.objects.get(email=values['email'])
            except DoesNotExist:
                return HTTPNotFound()

            if (user.password == values['password']):
                headers = remember(request, str(user._id))
                return HTTPFound(location='/', headers=headers)

        except ValidationFailure, e:
            form_render = e.render()
    else:
        form_render = form.render()

    params = {
        'form': Markup(form_render)
    }

    return render_to_response('user/login.html', params)


@view_config(route_name='user_register')
def register(request):

    schema = UserRegisterSchema(validator=user_register_validator)
    form = Form(schema, buttons=('submit',))

    userid = authenticated_userid(request)
    if userid:
        return HTTPFound(location='/')

    if 'submit' in request.POST:
        controls = request.POST.items()

        try:
            values = form.validate(controls)

            user = User(
                name=values['name'],
                email=values['email'],
                password=values['password'],
                created=int(time())
            ).save()

            headers = remember(request, str(user))
            return HTTPFound(location='/', headers=headers)

        except ValidationFailure, e:
            form_render = e.render()
    else:
        form_render = form.render()

    params = {
        'form': Markup(form_render)
    }

    return render_to_response('user/register.html', params)


@view_config(route_name='user_logout', permission='authenticated')
def logout(request):
    headers = forget(request)
    return HTTPFound(location='/user/login', headers=headers)
