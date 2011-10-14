var Triage = Triage || {};
Triage.modules = Triage.modules = {};

Triage.modules.tableAccordion = (function($, app) {
	"use strict";

	return {
		start: function() {
			$('table.accordion th').click(function() {
				var $body = $('table.accordion tbody');
				if ($body.is(':visible')) {
					$body.slideUp('fast');
				}
				else {
					$body.slideDown('fast');
				}
			});
		},
		stop: function() {
			$('table.accordion tbody').slideUp('fast');
		}
	};
});

Triage.modules.tableAccordion.autoRegister = true;