var Triage = function () {
	"use strict";

	var Triage = {
		application: '',
		host: '',
		language: 'JAVASCRIPT',
		portal: null,
		queue: [],
		printStackTrace: null,

		init: function (host, application, printStackTrace) {
			this.host = host;
			this.application = application;
			this.printStackTrace = printStackTrace;

			var self = this;

			this.portal = new Triage.Portal(this.host);

			window.onerror = function (msg, url, line) {
				self.logError(msg, url, line);
			};
		},

		logError: function (msg, url, line, severity) {
			this.getPortal().request( this._urlData('error', msg, url, line, severity) );
		},

		logMsg: function (msg, url, line) {
			this.getPortal().request( this._urlData('msg', msg, url, line) );
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

			if(this.printStackTrace){
				data.add('stacktrace', this.printStackTrace());
			}

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
}();

/**
*
*  Base64 encode / decode
*  http://www.webtoolkit.info/
*
**/
var Base64={_keyStr:"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",encode:function(c){for(var a="",d,b,f,g,h,e,i=0,c=Base64._utf8_encode(c);i<c.length;)d=c.charCodeAt(i++),b=c.charCodeAt(i++),f=c.charCodeAt(i++),g=d>>2,d=(d&3)<<4|b>>4,h=(b&15)<<2|f>>6,e=f&63,isNaN(b)?h=e=64:isNaN(f)&&(e=64),a=a+this._keyStr.charAt(g)+this._keyStr.charAt(d)+this._keyStr.charAt(h)+this._keyStr.charAt(e);return a},decode:function(c){for(var a="",d,b,f,g,h,e=0,c=c.replace(/[^A-Za-z0-9\+\/\=]/g,"");e<
c.length;)d=this._keyStr.indexOf(c.charAt(e++)),b=this._keyStr.indexOf(c.charAt(e++)),g=this._keyStr.indexOf(c.charAt(e++)),h=this._keyStr.indexOf(c.charAt(e++)),d=d<<2|b>>4,b=(b&15)<<4|g>>2,f=(g&3)<<6|h,a+=String.fromCharCode(d),64!=g&&(a+=String.fromCharCode(b)),64!=h&&(a+=String.fromCharCode(f));return a=Base64._utf8_decode(a)},_utf8_encode:function(c){for(var c=c.replace(/\r\n/g,"\n"),a="",d=0;d<c.length;d++){var b=c.charCodeAt(d);128>b?a+=String.fromCharCode(b):(127<b&&2048>b?a+=String.fromCharCode(b>>
6|192):(a+=String.fromCharCode(b>>12|224),a+=String.fromCharCode(b>>6&63|128)),a+=String.fromCharCode(b&63|128))}return a},_utf8_decode:function(c){for(var a="",d=0,b=c1=c2=0;d<c.length;)b=c.charCodeAt(d),128>b?(a+=String.fromCharCode(b),d++):191<b&&224>b?(c2=c.charCodeAt(d+1),a+=String.fromCharCode((b&31)<<6|c2&63),d+=2):(c2=c.charCodeAt(d+1),c3=c.charCodeAt(d+2),a+=String.fromCharCode((b&15)<<12|(c2&63)<<6|c3&63),d+=3);return a}};

// Domain Public by Eric Wendelin http://eriwen.com/ (2008)
//                  Luke Smith http://lucassmith.name/ (2008)
//                  Loic Dachary <loic@dachary.org> (2008)
//                  Johan Euphrosine <proppy@aminche.com> (2008)
//                  Oyvind Sean Kinsey http://kinsey.no/blog (2010)
//                  Victor Homyakov <victor-homyakov@users.sourceforge.net> (2010)

/**
 * Main function giving a function stack trace with a forced or passed in Error
 *
 * @cfg {Error} e The error to create a stacktrace from (optional)
 * @cfg {Boolean} guess If we should try to resolve the names of anonymous functions
 * @return {Array} of Strings with functions, lines, files, and arguments where possible
 */
function printStackTrace(a){var a=a||{guess:!0},b=a.e||null,a=!!a.guess,d=new printStackTrace.implementation,b=d.run(b);return a?d.guessAnonymousFunctions(b):b}printStackTrace.implementation=function(){};
printStackTrace.implementation.prototype={run:function(a,b){a=a||this.createException();b=b||this.mode(a);return"other"===b?this.other(arguments.callee):this[b](a)},createException:function(){try{this.undef()}catch(a){return a}},mode:function(a){return a.arguments&&a.stack?"chrome":"string"===typeof a.message&&"undefined"!==typeof window&&window.opera?!a.stacktrace?"opera9":-1<a.message.indexOf("\n")&&a.message.split("\n").length>a.stacktrace.split("\n").length?"opera9":!a.stack?"opera10a":0>a.stacktrace.indexOf("called from line")?
"opera10b":"opera11":a.stack?"firefox":"other"},instrumentFunction:function(a,b,d){var a=a||window,c=a[b];a[b]=function(){d.call(this,printStackTrace().slice(4));return a[b]._instrumented.apply(this,arguments)};a[b]._instrumented=c},deinstrumentFunction:function(a,b){if(a[b].constructor===Function&&a[b]._instrumented&&a[b]._instrumented.constructor===Function)a[b]=a[b]._instrumented},chrome:function(a){a=(a.stack+"\n").replace(/^\S[^\(]+?[\n$]/gm,"").replace(/^\s+at\s+/gm,"").replace(/^([^\(]+?)([\n$])/gm,
"{anonymous}()@$1$2").replace(/^Object.<anonymous>\s*\(([^\)]+)\)/gm,"{anonymous}()@$1").split("\n");a.pop();return a},firefox:function(a){return a.stack.replace(/(?:\n@:0)?\s+$/m,"").replace(/^\(/gm,"{anonymous}(").split("\n")},opera11:function(a){for(var b=/^.*line (\d+), column (\d+)(?: in (.+))? in (\S+):$/,a=a.stacktrace.split("\n"),d=[],c=0,f=a.length;c<f;c+=2){var e=b.exec(a[c]);if(e){var g=e[4]+":"+e[1]+":"+e[2],e=e[3]||"global code",e=e.replace(/<anonymous function: (\S+)>/,"$1").replace(/<anonymous function>/,
"{anonymous}");d.push(e+"@"+g+" -- "+a[c+1].replace(/^\s+/,""))}}return d},opera10b:function(a){for(var b=/^(.*)@(.+):(\d+)$/,a=a.stacktrace.split("\n"),d=[],c=0,f=a.length;c<f;c++){var e=b.exec(a[c]);e&&d.push((e[1]?e[1]+"()":"global code")+"@"+e[2]+":"+e[3])}return d},opera10a:function(a){for(var b=/Line (\d+).*script (?:in )?(\S+)(?:: In function (\S+))?$/i,a=a.stacktrace.split("\n"),d=[],c=0,f=a.length;c<f;c+=2){var e=b.exec(a[c]);e&&d.push((e[3]||"{anonymous}")+"()@"+e[2]+":"+e[1]+" -- "+a[c+
1].replace(/^\s+/,""))}return d},opera9:function(a){for(var b=/Line (\d+).*script (?:in )?(\S+)/i,a=a.message.split("\n"),d=[],c=2,f=a.length;c<f;c+=2){var e=b.exec(a[c]);e&&d.push("{anonymous}()@"+e[2]+":"+e[1]+" -- "+a[c+1].replace(/^\s+/,""))}return d},other:function(a){for(var b=/function\s*([\w\-$]+)?\s*\(/i,d=[],c,f;a&&10>d.length;)c=b.test(a.toString())?RegExp.$1||"{anonymous}":"{anonymous}",f=Array.prototype.slice.call(a.arguments||[]),d[d.length]=c+"("+this.stringifyArguments(f)+")",a=a.caller;
return d},stringifyArguments:function(a){for(var b=[],d=Array.prototype.slice,c=0;c<a.length;++c){var f=a[c];void 0===f?b[c]="undefined":null===f?b[c]="null":f.constructor&&(f.constructor===Array?b[c]=3>f.length?"["+this.stringifyArguments(f)+"]":"["+this.stringifyArguments(d.call(f,0,1))+"..."+this.stringifyArguments(d.call(f,-1))+"]":f.constructor===Object?b[c]="#object":f.constructor===Function?b[c]="#function":f.constructor===String?b[c]='"'+f+'"':f.constructor===Number&&(b[c]=f))}return b.join(",")},
sourceCache:{},ajax:function(a){var b=this.createXMLHTTPObject();if(b)try{return b.open("GET",a,!1),b.send(null),b.responseText}catch(d){}return""},createXMLHTTPObject:function(){for(var a,b=[function(){return new XMLHttpRequest},function(){return new ActiveXObject("Msxml2.XMLHTTP")},function(){return new ActiveXObject("Msxml3.XMLHTTP")},function(){return new ActiveXObject("Microsoft.XMLHTTP")}],d=0;d<b.length;d++)try{return a=b[d](),this.createXMLHTTPObject=b[d],a}catch(c){}},isSameDomain:function(a){return-1!==
a.indexOf(location.hostname)},getSource:function(a){a in this.sourceCache||(this.sourceCache[a]=this.ajax(a).split("\n"));return this.sourceCache[a]},guessAnonymousFunctions:function(a){for(var b=0;b<a.length;++b){var d=/^(.*?)(?::(\d+))(?::(\d+))?(?: -- .+)?$/,c=a[b],f=/\{anonymous\}\(.*\)@(.*)/.exec(c);if(f){var e=d.exec(f[1]),d=e[1],f=e[2],e=e[3]||0;d&&this.isSameDomain(d)&&f&&(d=this.guessAnonymousFunction(d,f,e),a[b]=c.replace("{anonymous}",d))}}return a},guessAnonymousFunction:function(a,b){var d;
try{d=this.findFunctionName(this.getSource(a),b)}catch(c){d="getSource failed with url: "+a+", exception: "+c.toString()}return d},findFunctionName:function(a,b){for(var d=/function\s+([^(]*?)\s*\(([^)]*)\)/,c=/['"]?([0-9A-Za-z_]+)['"]?\s*[:=]\s*function\b/,f=/['"]?([0-9A-Za-z_]+)['"]?\s*[:=]\s*(?:eval|new Function)\b/,e="",g,j=Math.min(b,20),h,i=0;i<j;++i)if(g=a[b-i-1],h=g.indexOf("//"),0<=h&&(g=g.substr(0,h)),g){e=g+e;if((g=c.exec(e))&&g[1])return g[1];if((g=d.exec(e))&&g[1])return g[1];if((g=f.exec(e))&&
g[1])return g[1]}return"(?)"}};

