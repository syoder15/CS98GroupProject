function validateEmail(formName){
	var email = document.forms[formName]["email"].value;
	var at = email.indexOf("@");
	var period = email.lastIndexOf(".");
	if (at < 1 || period < at + 2 || period + 2 >= email.length)
		alert("Please enter a valid email address");
		return false;
	}
}

function requiredField(formName, fields){
	for x in fields:
		var field = document.forms[formName][fieldName].value;
		if (field==null || field==''){
		alert("Please fill out all Required Fields.")
	}

}