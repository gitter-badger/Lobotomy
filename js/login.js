/*
 * filename: login.js
 * last modified: 04/01/2012
*/

// login/register tabs
lga_loginTabs = {
	init: function() {
		$("ul.login_tabs").flowtabs("div.login_panes > div", {
				onBeforeClick: function(event, tabIndex) {
					if(typeof validator != 'undefined') {
						validator.resetForm(); //reset validator when switching tabs
					}
				}
			}
		);
	}
}

// add class focus to active form element
lga_formFocus = {
	init: function() {
		$('input, textarea').bind('focus blur', function(){
			$(this).toggleClass('focus');
		})
	}
}

// form validation
lga_validation = {
	init: function() {
		validator = $("#form_login").validate({
			rules: {
				lusername: "required",
				lpassword: "required"
			},
			messages: {
				lusername: "<strong>Username</strong> is required (type anything)",
				lpassword: "<strong>Password</strong> is required (type anything)"
			},
			errorLabelContainer: $("#allErrors")
		});
	}
}
