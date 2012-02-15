Triage.modules.dropdown = (function($, app) {
	"use strict";

	return {
		start: function() {
			$('.dropdown-toggle').dropdown();
		    $('body').tooltip({
		      selector: ".tooltip-toggle"
		    });		
		},
		stop: function() {
		}
	};
});

Triage.modules.dropdown.autoRegister = true;