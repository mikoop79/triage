Triage.modules.tableAccordion = (function($, app) {
	"use strict";

	return {
		start: function() {
			$(function() {
				$("[data-tablesort]").tablesorter();
			});
		},
		stop: function() { }
	};
});

Triage.modules.tableAccordion.autoRegister = true;
