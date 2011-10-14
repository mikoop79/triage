from pymongo.code import Code


def get_errors(request, collection):

	map = Code("""

	function() {
	  emit( this.type +":"+ this.line +":"+ this.file, {
	    message: this.message,
	    type: this.type,
	    line: this.line,
	    file: this.file,
	    oldest: this.timestamp,
	    youngest: this.timestamp,
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
	      result._id = value._id;
	    }
	    if (value.youngest > result.youngest) {
	      result.message = value.message;
	      result.youngest = value.youngest;
	    }

	    result.count += value.count;
	  });
	  return result;
	}""")
	return request.db[collection].map_reduce(map, reduce, collection+'aggregate').find(fields={ 'value': 1 })