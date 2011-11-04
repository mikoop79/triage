var Triage = function() {
	"use strict";

	var Triage = {
		application: '',
		host: '',
		language: 'JAVASCRIPT',
		portal: null,
		queue: [],

		init: function(host, application) {
			this.host = host;
			this.application = application;

			var self = this;

			window.onerror = function(msg, url, line) {
				self.logError(msg, url, line);
			};
		},

		logError: function(exception, url, line) {
			this.getPortal().request(this._urlData('error', exception, url, line));
		},

		logMsg: function(msg, url, line) {
			this.getPortal().request(this._urlData('msg', msg, url, line));
		},

		_urlData: function(name, exception, url, line) {
			var data = new Triage.UrlData();
			data
				.add('application', this.application)
				.add('host', this.host)
				.add('language', this.language)
				.add('level', name)
				.add('line', line)
				.add('type', 'exception')
				.add('message', exception);

			return data.output();
		},

		getPortal: function(){
			if(this.portal === null){
				this.portal = new Triage.Portal(this.host);
			}

			return this.portal;
		}
	}

	Triage.Exception = function(msg, severity){
		this.msg = msg;
		this.severity = severity;

		return "Triage.Exception: { 'msg': "+msg+", 'severity': "+severity+" }";
	}

	Triage.UrlData = function() {
		var data = '?';

		this.add = function (name, value) {
			data += name + '=' + encodeURIComponent(value) + '&';

			return this;
		}

		this.output = function(){
			return data;
		}

		return this;
	}

	Triage.Portal = function(host){
		var iframe = document.createElement('iframe');
		iframe.style.width   = '1px';
		iframe.style.height  = '1px';
		iframe.style.display = 'none';
		
		this.portal = iframe;

		if (document.body) {
			document.body.appendChild(iframe);
		} else {
			_onWindowLoad(function(){
				document.body.appendChild(iframe);
			});
		}

		/** public functions **/

		this.request = function(data){
			iframe.src = _getUrl(data);
		}

		/** private functions **/

		function _onWindowLoad(callback){
			var previousOnload = window.onload;

			if(typeof window.onload != 'function'){
				window.onload = callback;
				return;
			}

			window.onload = function(){
				if(previousOnload){
					previousOnload();
				}

				callback();
			};
		}

		function _getUrl(data){
			return 'http://'+host + '/api/log?'+data;
		}

		return this;
	}

	return Triage;
}()


