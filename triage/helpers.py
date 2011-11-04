from pymongo.code import Code
from pymongo import DESCENDING

def get_errors(request, project, show):

	map = Code("""

	function() {
		emit( this.type +":"+ this.line +":"+ this.file, {
			message: this.message,
			type: this.type,
			line: this.line,
			file: this.file,
			oldest: this.timestamp,
			youngest: this.timestamp,
			hidden: this.hidden,
			seen: this.seen,
			_id: this._id,
			count:1 
		});
	}""")

	reduce = Code("""

	function(key, values) {
		var result = values.pop();

		values.forEach(function(value) {
			if (value.oldest < result.oldest) {
				result.oldest = value.oldest;
			}
			if (value.youngest > result.youngest) {
				result.message = value.message;
				result.youngest = value.youngest;
				result._id = value._id;
			}
			result.hidden = (result.hidden || value.hidden);
			result.seen = (result.seen || value.seen)
			result.count += value.count;
		});
		return result;
	}""")

	if show == 'all':
		where = None
	elif show == 'hidden':
		where = { 'value.hidden': 1 }
	elif show == 'seen':
		where = { 'value.seen': 1 }
	elif show == 'unseen':
		where = { 'value.seen': { '$ne': 1 }}

	collection = project['collection']

	return (request.db[collection]
		.map_reduce(map, reduce, collection+'-aggregate')
		.find(where)
		.sort('value.youngest', DESCENDING)
	)


def get_error_counts(request, project, show):

	pass
