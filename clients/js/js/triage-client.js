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
			
			this.portal = new Triage.Portal(this.host);

			window.onerror = function(msg, url, line) {
				self.logError(msg, url, line);
			};
		},

		flush: function(){
			this.getPortal().executeRequest();
		},

		logError: function(msg, url, line, severity) {
			this.getPortal().request(this._urlData('error', msg, url, line, severity));
		},

		logMsg: function(msg, url, line) {
			this.getPortal().request(this._urlData('msg', msg, url, line));
		},

		_urlData: function(name, exception, url, line, severity) {
			var data = new Triage.UrlData();
			data
				.add('application', this.application)
				.add('host', this.host)
				.add('language', this.language)
				.add('level', name)
				.add('line', line)
				.add('type', 'exception')
				.add('message', exception)
								
				//Context data
				.add('url', url)
				.add('useragent', navigator.userAgent)
				.add('cookies', document.cookie);

			if(severity){
				data.add('severity', severity)				
			}

			return data.output();
		},

		getPortal: function(){
			return this.portal;
		}		
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
		var queue = [];
		var iframe = null;
		var self = this;

		/** Setup iframe **/
		iframe = document.createElement('iframe');
		iframe.style.width   = '1px';
		iframe.style.height  = '1px';
		iframe.style.display = 'none';
		
		iframe.onload = function() {
			if(queue.length > 0){
				self.executeRequest();
			}
		}

		if (document.body) {
			document.body.appendChild(iframe);
		} else {
			_onWindowLoad(function(){
				document.body.appendChild(iframe);
			});
		}

		/** public functions **/

		this.request = function(data){
			queue.push(_getUrl(data));

			if (queue.length === 1) {
				this.executeRequest();
			}
		}

		this.executeRequest = function() {
			iframe.src = queue[0];
			queue.shift();
		}

		/** private functions **/

		function _onWindowLoad(callback) {
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
			return 'http://'+host + '/api/log'+data;
		}


		return this;
	}

	return Triage;
}()

Triage.init('127.0.0.1:6543', 'frontend');		

