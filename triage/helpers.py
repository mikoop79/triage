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

	collection = project['collection']

	last_reduced = get_last_reduced(request, collection)

	result = (request.db[collection]
		.map_reduce(map, reduce, out={'reduce': collection+'-aggregate'}, query={'timestamp': {'$gt':last_reduced}})
		.find(get_filter(show))
		.sort('value.youngest', DESCENDING)
	)
	set_last_reduced(request, collection)

	return result	


def set_last_reduced(request, collection):
	request.db['triage'].update(
		{ 'collection': collection, 'lastreduced' : True },
		{ 'collection': collection, 'lastreduced' : True, 'time': time() },
		upsert=True
	)


def get_last_reduced(request, collection):
	doc = request.db['triage'].find_one({ 'collection': collection, 'lastreduced' : True })
	if doc:
		return doc['time']
	return 0



def get_error_count(request, project, show):
	collection = project['collection']+'-aggregate'
	return request.db[collection].find(get_filter(show)).count()


def get_filter(show):
	if show == 'all':
		return None
	elif show == 'hidden':
		return { 'value.hidden': True }
	elif show == 'seen':
		return { 'value.seen': True, 'value.hidden': { '$ne': True }}
	elif show == 'unseen':
		return { 'value.seen': { '$ne': True }, 'value.hidden': { '$ne': True }}

