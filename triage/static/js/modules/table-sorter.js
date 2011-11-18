Triage.modules.tableAccordion = (function($, app) {
	"use strict";

	return {
		start: function() {
			$(function() {
				$("[data-tablesort]").tablesorter({ sortList: [[1,0]] });
			});
		},
		stop: function() { }
	};
});

Triage.modules.tableAccordion.autoRegister = true;
