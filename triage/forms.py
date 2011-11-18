from colander import MappingSchema
from colander import SchemaNode
from colander import String


class CommentsSchema(MappingSchema):

	name = SchemaNode(String(),
						description='Your name')

	comment = SchemaNode(String(),
						description='Your comment')
