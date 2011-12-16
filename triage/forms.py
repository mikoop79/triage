from colander import MappingSchema, SchemaNode
from colander import String, Email
from colander import Invalid
from deform.widget import PasswordWidget, TextAreaWidget
import pyramid.threadlocal as threadlocal


def user_register_validator(form, values):
    exception = Invalid(form, 'There was a problem with your submission')
    if values['password'] != values['confirm_password']:
        exception['confirm_password'] = 'Confirm Password does not match Password'

    email = values['email']
    user = threadlocal.get_current_request().db['users'].find_one({'email': email})
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
