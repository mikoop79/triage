from colander import MappingSchema, SchemaNode
from colander import String, Email
from colander import Invalid
from deform.widget import PasswordWidget, TextAreaWidget, TextInputWidget
from triage.models import User
from passlib.apps import custom_app_context as pwd_context
from colander import Invalid

def user_login_validator(form, values):
    try:
        user = User.objects.get(email=values['email'])

        if (not pwd_context.verify(values['password'], user.password)):
            raise exception
    except:
        exception = Invalid(form, 'There was a problem with your submission')
        exception['email'] = 'Your Email or Password is incorrect'
        raise exception


def user_register_validator(form, values):
    exception = Invalid(form, 'There was a problem with your submission')
    if values['password'] != values['confirm_password']:
        exception['confirm_password'] = 'Confirm Password does not match Password'

    user = User.objects(name=values['name'])
    if user:
        exception['name'] = 'You have to choose a unique name'

    user = User.objects(email=values['email'])
    if user:
        exception['email'] = 'Email already exists in our database'

    if exception.children:
        raise exception


class CommentsSchema(MappingSchema):
    comment = SchemaNode(String(), description='Your comment', widget=TextAreaWidget())


class UserLoginSchema(MappingSchema):
    email = SchemaNode(String(), description='Enter your email address', validator=Email())
    password = SchemaNode(String(), description='Enter your password', widget=PasswordWidget())


class UserRegisterSchema(MappingSchema):
    name = SchemaNode(String(), descriprtion='Enter your name')
    email = SchemaNode(String(), description='Enter your email address', validator=Email())
    password = SchemaNode(String(), description='Enter your password', widget=PasswordWidget())
    confirm_password = SchemaNode(String(), description='Confirm your password', widget=PasswordWidget())


class TagSchema(MappingSchema):
    tag = SchemaNode(String(), description='Enter a descriptive tag', widget=TextInputWidget())
