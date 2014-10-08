$(document).ready(function() {
	var uField = $("#id_username");
	var pField = $("#id_password");
	
	// Add 'Username'/'Password' to fields
	$(uField).val("Username");
	$(pField).val("Password");
	$(pField).attr('type', 'text');
	
	// Show/hide: 'Username' in field on focus/focusout
	$(uField).focus(function() {
		$(uField).val("");
		$(uField).css("color", "black");
	});
	$(uField).focusout(function() {
		if ($(uField).val() == "") {
			$(uField).val("Username");
			$(uField).css("color", "#999999");
		}
	});
	
	// Show/hide: 'Password' in field on focus/focusout
	$(pField).focus(function() {
		$(pField).val("");
		$(pField).attr('type', 'password');
		$(pField).css("color", "black");
	});
	$(pField).focusout(function() {
		if ($(pField).val() == "") {
			$(pField).val("Password");
			$(pField).attr('type', 'text');
			$(pField).css("color", "#999999");
		}
	});
	
	
});