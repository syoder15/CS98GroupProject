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
};

function timeValidation(time) {
	if ( time.indexOf(':') < 0 ) {
		alert('Your time must include a colon (:)');
		return false;
	}

	var splitTime = time.split(':');
	var splitMinute = splitTime[1].split(' ');

	if ( splitTime[0] > 24 || splitMinute[0] > 59 ) {
		alert("You must enter a valid time");
		return false;
	}

	if ( splitMinute[1] !== 'AM' && splitMinute[1] !== 'PM' ) {
		alert("You must enter a valid time including either 'AM' or 'PM'.");
		return false;
	} 
};

function startEndTimeValidation(startTime, endTime) {
	var startTime = startTime.split(':');
	var endTime = endTime.split(':');
	var startMin = startTime[1].split(" ");
	var endMin = endTime[1].split(" ");

	if (startMin[1] == 'PM') {
		startTime[0] += 12;
	}

	if (endMin[1] == 'PM') {
		endTime[0] += 12;
	}

	if ( endTime[0] < startTime[0] ) {
		alert("Your start time must be before your end time. Please try again.");
		return false;
	}

	

	if (endTime[0] == startTime[0] && endMin[0] < startMin[0]) {
		alert("Your start time must be before your end time. Please try again.");
		return false;
	}
};

/*
 * dateValidation
 * input date expects a date in the format YYYY-MM-DD
 * Returns false if a date is invalid, true otherwise
 * Checks to see if a date is in the past (before the current date) and if the month and day exist
 */
function dateValidation(date) {
	var currentDate = getCurrentDate();

	var year = +date.substring(0, 4);
	var month = +date.substring(5, 7);
	var day = +date.substring(8, 10);

	if (date.length < 10) {
		alert('Please enter your date in the format YYYY-MM-DD');
		return false;
	}

	if (year < currentDate['year'] || (month < currentDate['month'] && year == currentDate['year'])
		|| (month == currentDate['month'] && year == currentDate['year'] && day < currentDate['date'])) {
		alert ('You cannot enter a date that is in the past. Please try again.');
		return false;
	} else if ( month >  12 || day > 31) {
		alert('You must enter a valid date. Please try again.');
		return false;
	}

	return true;
};

/*
 * getCurrentDate function
 * Gets the current date using built-in Javascript functionality
 * Returns the day, month, and year in an associative array
 */
function getCurrentDate() {
	var today = new Date();

	var day = today.getDate();
	var month = today.getMonth() + 1;
	var year = today.getFullYear();

	if (day < 10) {
		day = '0'+day;
	}
	if (month < 10) {
		month = '0'+month;
	}

	var currentDate = {
		'date': day,
		'month': month,
		'year': year
	};

	return currentDate;
}