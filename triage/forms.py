from colander import MappingSchema
from colander import SchemaNode
from colander import String, Email
from deform.widget import PasswordWidget, TextAreaWidget


class CommentsSchema(MappingSchema):

    name = SchemaNode(String(), description='Your name')

    comment = SchemaNode(String(), description='Your comment', widget=TextAreaWidget())


class UserLoginSchema(MappingSchema):

    email = SchemaNode(String(), description='Enter your email address', validator=Email())

    password = SchemaNode(String(), description='Enter your password', widget=PasswordWidget())
