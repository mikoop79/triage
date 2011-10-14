/* bootstrap-dropdown.js v1.3.0
 * http://twitter.github.com/bootstrap/javascript.html#dropdown
 */
!function(a){function c(){a(b).parent("li").removeClass("open")}a.fn.dropdown=function(e){return this.each(function(){a(this).delegate(e||b,"click",function(b){var d=a(this).parent("li"),e=d.hasClass("open");c();!e&&d.toggleClass("open");return false})})};var b="a.menu, .dropdown-toggle";a(function(){a("html").bind("click",c);a("body").dropdown("[data-dropdown] a.menu, [data-dropdown] .dropdown-toggle")})}(window.jQuery||window.ender)