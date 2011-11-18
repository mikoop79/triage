var Triage = function () {
	"use strict";

	var Triage = {
		application: '',
		host: '',
		language: 'JAVASCRIPT',
		portal: null,
		queue: [],

		init: function (host, application) {
			this.host = host;
			this.application = application;

			var self = this;

			this.portal = new Triage.Portal(this.host);

			window.onerror = function (msg, url, line) {
				self.logError(msg, url, line);
			};
		},

		logError: function (msg, url, line, severity) {
			this.getPortal().request(this._urlData('error', msg, url, line, severity));
		},

		logMsg: function (msg, url, line) {
			this.getPortal().request(this._urlData('msg', msg, url, line));
		},

		_urlData: function (name, exception, url, line, severity) {
			var data = new Triage.UrlData();
			data
				.add('application', this.application)
				.add('host', this.host)
				.add('language', this.language)
				.add('level', name)
				.add('line', line)
				.add('type', 'error')
				.add('message', exception)

				.add('context', {
					'url' : url,
					'useragent' : navigator.userAgent,
					'cookies' : document.cookie,
					'host' : this.host
				})

			if (severity) {
				data.add('severity', severity)
			}

			return '?data='+data.output();
		},

		getPortal: function(){
			return this.portal;
		}
	}

	Triage.UrlData = function() {
		var data = {};

		this.add = function (name, value) {
			data[name] = value;

			return this;
		}

		this.output = function(){
			return Base64.encode(JSON.stringify(data));
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

/**
*
*  Base64 encode / decode
*  http://www.webtoolkit.info/
*
**/

var Base64 = {

	// private property
	_keyStr : "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",

	// public method for encoding
	encode : function (input) {
		var output = "";
		var chr1, chr2, chr3, enc1, enc2, enc3, enc4;
		var i = 0;

		input = Base64._utf8_encode(input);

		while (i < input.length) {

			chr1 = input.charCodeAt(i++);
			chr2 = input.charCodeAt(i++);
			chr3 = input.charCodeAt(i++);

			enc1 = chr1 >> 2;
			enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
			enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
			enc4 = chr3 & 63;

			if (isNaN(chr2)) {
				enc3 = enc4 = 64;
			} else if (isNaN(chr3)) {
				enc4 = 64;
			}

			output = output +
			this._keyStr.charAt(enc1) + this._keyStr.charAt(enc2) +
			this._keyStr.charAt(enc3) + this._keyStr.charAt(enc4);

		}

		return output;
	},

	// public method for decoding
	decode : function (input) {
		var output = "";
		var chr1, chr2, chr3;
		var enc1, enc2, enc3, enc4;
		var i = 0;

		input = input.replace(/[^A-Za-z0-9\+\/\=]/g, "");

		while (i < input.length) {

			enc1 = this._keyStr.indexOf(input.charAt(i++));
			enc2 = this._keyStr.indexOf(input.charAt(i++));
			enc3 = this._keyStr.indexOf(input.charAt(i++));
			enc4 = this._keyStr.indexOf(input.charAt(i++));

			chr1 = (enc1 << 2) | (enc2 >> 4);
			chr2 = ((enc2 & 15) << 4) | (enc3 >> 2);
			chr3 = ((enc3 & 3) << 6) | enc4;

			output = output + String.fromCharCode(chr1);

			if (enc3 != 64) {
				output = output + String.fromCharCode(chr2);
			}
			if (enc4 != 64) {
				output = output + String.fromCharCode(chr3);
			}

		}

		output = Base64._utf8_decode(output);

		return output;

	},

	// private method for UTF-8 encoding
	_utf8_encode : function (string) {
		string = string.replace(/\r\n/g,"\n");
		var utftext = "";

		for (var n = 0; n < string.length; n++) {

			var c = string.charCodeAt(n);

			if (c < 128) {
				utftext += String.fromCharCode(c);
			}
			else if((c > 127) && (c < 2048)) {
				utftext += String.fromCharCode((c >> 6) | 192);
				utftext += String.fromCharCode((c & 63) | 128);
			}
			else {
				utftext += String.fromCharCode((c >> 12) | 224);
				utftext += String.fromCharCode(((c >> 6) & 63) | 128);
				utftext += String.fromCharCode((c & 63) | 128);
			}

		}

		return utftext;
	},

	// private method for UTF-8 decoding
	_utf8_decode : function (utftext) {
		var string = "";
		var i = 0;
		var c = c1 = c2 = 0;

		while ( i < utftext.length ) {

			c = utftext.charCodeAt(i);

			if (c < 128) {
				string += String.fromCharCode(c);
				i++;
			}
			else if((c > 191) && (c < 224)) {
				c2 = utftext.charCodeAt(i+1);
				string += String.fromCharCode(((c & 31) << 6) | (c2 & 63));
				i += 2;
			}
			else {
				c2 = utftext.charCodeAt(i+1);
				c3 = utftext.charCodeAt(i+2);
				string += String.fromCharCode(((c & 15) << 12) | ((c2 & 63) << 6) | (c3 & 63));
				i += 3;
			}

		}

		return string;
	}

}

Triage.init('127.0.0.1:6543', 'frontend');

