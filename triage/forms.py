from colander import MappingSchema, SchemaNode
from colander import String, Email
from colander import Invalid
from deform.widget import PasswordWidget, TextAreaWidget
from triage.models import User


def user_login_validator(form, values):
    try:
        User.objects.get(email=values['email'])
    except:
        exception = Invalid(form, 'There was a problem with your submission')
        exception['email'] = 'Your Email or Password is incorrect'
        raise exception


def user_register_validator(form, values):
    exception = Invalid(form, 'There was a problem with your submission')
    if values['password'] != values['confirm_password']:
        exception['confirm_password'] = 'Confirm Password does not match Password'

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

    email = SchemaNode(String(), description='Enter your email address', validator=Email())

    password = SchemaNode(String(), description='Enter your password', widget=PasswordWidget())

    confirm_password = SchemaNode(String(), description='Confirm your password', widget=PasswordWidget())
