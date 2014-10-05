function validateEmail(formName){
	var email = document.forms[formName]["email"].value;
	var at = email.indexOf("@");
	var period = email.lastIndexOf(".");
	if (at < 1 || period < at + 2 || period + 2 >= email.length) {
		alert("Please enter a valid email address");
		return false;
	}
};

function validatePhoneNumber(formName) {
	var number = document.forms[formName]['phone_number'].value;
	//number = number.replace(/[()]-/g, '');
	number = number.replace(/\)\s*|\(\s*|-/g, '');
	return number;
}