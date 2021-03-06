function validateEmail(email){
	var at = email.indexOf("@");
	var period = email.lastIndexOf(".");

	if ((at < 1 || period < at + 2 || period + 2 >= email.length) && email.length != 0) {
		//alert("Please enter a valid email address");
		return "Please enter a valid email address";
	}
	return "";
};

function validatePhoneNumber(number) {
	phone = number.replace(/[^0-9]/g, '');
	console.log('got here');
	if(! (phone.match(/\d/g) && phone.length==10) && number.length!=0){
		console.log("invalid");
		return "Please enter a valid phone number";
	}
	else{
		console.log('valid');
		phone = phone.replace(/\)\s*|\(\s*|-/g, '');
		$('#phone_number_input').val(phone);
		return '';
	}

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

	if(typeof splitMinute[1] !== 'undefined'){
		if ( splitMinute[1].toUpperCase() !== 'AM' && splitMinute[1].toUpperCase() !== 'PM' && 
			splitMinute[1].toUpperCase() !== 'P.M.' && splitMinute[1].toUpperCase() !== 'A.M.' ) {
			alert("You must enter a valid time including either 'AM' or 'PM'.");
			return false;
		} 
	}	

	return true;
};

function startEndTimeValidation(startTime, endTime) {
	var start_time =  startTime.split(':');
	var end_time = endTime.split(':');

	if ( startTime.indexOf(':') < 0 || endTime.indexOf(':') < 0 ) {
		var msg = 'Your time must include a colon (:)';
		return msg;
	}

	var startMin = start_time[1].split(" ");
	var endMin = end_time[1].split(" ");

	if (typeof(startMin[1]) !== 'undefined' && ( startMin[1].toLowerCase() == 'p.m.'  || startMin[1].toLowerCase() == 'pm' ) ){
		startMin[1] = 'PM';
		if (parseInt(start_time[0]) !== 12) { 
			start_time[0] = parseInt(start_time[0]) + 12;
		}
		console.log("start Time is " + start_time[0]);
	}

	if ( (typeof(endMin[1]) !== 'undefined') &&  ( endMin[1].toLowerCase() == 'p.m.' || endMin[1].toLowerCase() == 'pm' )) {
		endMin[1] = 'PM';
		if (parseInt(end_time[0]) !== 12) { 
			end_time[0] = parseInt(end_time[0]) + 12;
		}
		console.log("end Time is " + end_time[0]);
	}

	if ( end_time[0] < start_time[0] ) {
		//alert("Your start time must be before your end time. Please try again.");
		var msg = "Your start time must be before your end time. Please try again.";
		return msg;
	}

	if (end_time[0] == start_time[0] && parseInt(endMin[0]) < parseInt(startMin[0])) {
		//alert("Your start time must be before your end time. Please try again.");
		var msg = "Your start time must be before your end time. Please try again.";
		return msg;
	}

	return true;
};

/*
 * dateValidation
 * input date expects a date in the format YYYY-MM-DD
 * Returns false if a date is invalid, true otherwise
 * Checks to see if a date is in the past (before the current date) and if the month and day exist
 */
function dateValidation(date) {
	if (!date) {
		return true;
	}

	var currentDate = getCurrentDate();

	var year = +date.substring(0, 4);
	var month = +date.substring(5, 7);
	var day = +date.substring(8, 10);

	if (date.length < 10 || date.substring(4,5) != '-' || date.substring(7,8) != '-') {
		return 'Please enter your date in the format YYYY-MM-DD';
		//		  document.getElementById(dt).style.background ='#e35152';

	}

	 if ( month >  12 || month < 1 || day > 31  || month < 1 || year > 2050 ) {
		return 'You must enter a valid date. Please try again.';
		 //		  document.getElementById(dt).style.background ='#e35152';

	}
	else if (year < currentDate['year'] || (month < currentDate['month'] && year == currentDate['year'])
		|| (month == currentDate['month'] && year == currentDate['year'] && day < currentDate['date'])) {
		 return 'You cannot enter a date that is in the past.';
		 // document.getElementById(dt).style.background ='#e35152';

	} 

	return true;
};

function isValidDate(formName)
{
	var dateString = document.forms[formName]["deadline"].value;
    // First check for the pattern
    var regex_date = /^\d{4}\-\d{1,2}\-\d{1,2}$/;
    console.log(dateString);
    if (dateString) {

	    if(!regex_date.test(dateString))
	    {
	    	alert('Please enter your date in the format YYYY-MM-DD');
	        return false;
	    }

	    // Parse the date parts to integers
	    var parts   = dateString.split("-");
	    var day     = parseInt(parts[2], 10);
	    var month   = parseInt(parts[1], 10);
	    var year    = parseInt(parts[0], 10);

	    // Check the ranges of month and year
	    if(year < 1000 || year > 3000 || month == 0 || month > 12)
	    {
	        return false;
	    }

	    var monthLength = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ];

	    // Adjust for leap years
	    if(year % 400 == 0 || (year % 100 != 0 && year % 4 == 0))
	    {
	        monthLength[1] = 29;
	    }

	    // Check the range of the day
	    return day > 0 && day <= monthLength[month - 1];
	} else {
		return true;
	}
}

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