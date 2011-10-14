function Application($, ns) {
	this.modules = [];
	this.events = {};
	this.$ = $;
	this.ns = ns;
	this.autoRegister();
}

Application.prototype.register = function(moduleDef, options) {
	if (!moduleDef.isRegistered) {
		this.modules.push(moduleDef(this.$, this, options));
		moduleDef.isRegistered = true;
	}
}

Application.prototype.autoRegister = function() {
	for (var moduleDef in this.ns.modules) {
		moduleDef = this.ns.modules[moduleDef];
		if (moduleDef.autoRegister)
			this.register(moduleDef);
	}	
}

Application.prototype.start = function() {
	for (var module in this.modules) {
		module = this.modules[module];
		module.start();
	}	
}

Application.prototype.stop = function() {
	for (var module in this.modules) {
		module = this.modules[module];
		module.stop();
	}	
}