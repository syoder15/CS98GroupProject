var addContact = $('.addcontact');
var addCompany = $('.addcompany');;
var addEvent = $('.addevent');;
var profileDropDown = $('.profileNameButton');
var contactForm = $('.contact_form');
var companyForm = $('.company_form');
var eventForm = $('.event_form');
var addFileButton = $("#id_filep");

function importMain(){
    var x = document.createElement('script');
    x.src = '../js/main.js';
    document.getElementsByTagName("head"[0]).appendChild(x);
}

addContact.on('click', function(){
	var contactOverlay = document.getElementById('contact_overlay');
	contactOverlay.style.display = "block";
});

addCompany.on('click', function(){
	var companyOverlay = document.getElementById('company_overlay')
	companyOverlay.style.display = "block";
});

addEvent.on('click', function(){
	var eventOverlay = document.getElementById('event_overlay')
	eventOverlay.style.display = "block";
});

profileDropDown.on('click', function() {
	$('.dropdown').toggleClass('visible');
});

addFileButton.hover(function(){
	console.log('HOVERING');
	$("#format_reminder").attr({"opacity" : "1"});
});


addFileButton.on('change', function() {
	console.log("HERE");
  	$('#company_name_input').removeAttr('required');
  	$('#company_deadline_input').removeAttr('required');
});


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

//validating company deeadline
function validateDeadline(){
	var deadline = $('#company_deadline_input').val();
	var msg = dateValidation(deadline);
	if(msg.length > 0){
		$('.error-message').show();
		$('#company_deadline_input').css('border','solid 2px red');
		$('.error-message').html(msg);
	}
	else{
		$('.error-message').hide();
		$('#company_deadline_input').css('border','solid 0px red');
	}
	return msg;
}

function validatePhone(){
	var number = $('#phone_number_input').val();
	console.log("PHONE NUMBER" + number);
	var msg = validatePhoneNumber(number);
	if(msg.length > 0){
		$('.phone_error_message').show();
		$('#phone_number_input').css('border','solid 2px red');
		$('.phone_error_message').html(msg);
	}
	else{
		$('.phone_error_message').hide();
		$('#phone_number_input').css('border','solid 0px red');
	}
	return msg;
}

function validateEmailAddress(){
	var email = $('#email_input').val();
	var msg = validateEmail(email);
	if(msg.length > 0){
		$('.email_error_message').show();
		$('#email_input').css('border','solid 2px red');
		$('.email_error_message').html(msg);
	}
	else{
		$('.email_error_message').hide();
		$('#email_input').css('border','solid 0px red');
	}
	return msg;
}

contactForm.submit(function(event){
	if(validateEmailAddress() !='' || validatePhone() !=''){
		return false;
	}

});

//don't let form submit if there's a date error!
companyForm.submit(function(event) {
	var error = 0;
	if (validateDeadline() != ""){
		return false;
	}

});


/*contactForm.submit(function(event) {

	if (validateDeadline() != ""){
		return false;
	}

  	event.preventDefault();
  	//NEED TO VALIDATE FIELDS
  	$('#contactModal').modal('hide');
  	var name = $('#name_input').val();
  	var phone = $('#phone_number_input').val();
  	var email = $('#email_input').val();
  	var company = $('#company_input').val();
  	var notes = $('#contact_notes_input').val();
	var csrftoken = getCookie('csrftoken');

	var formName = $('.contact_form').attr('name');
    validateEmail(formName);
    phone = validatePhoneNumber(formName);

  	$.ajaxSetup({
	    beforeSend: function(xhr, settings) {
		    xhr.setRequestHeader("X-CSRFToken", csrftoken);
	    }
	});
  	$.ajax({
  		type: "POST",
		url: "new_contact/",
		data: {
			"name": name,
			"phone": phone,
			"email": email,
			"company": company,
			"notes":notes
		}
	}).done(function() {
		console.log("GOT HERE");
		$( this ).addClass( "done" );
	});
});
*/

eventForm.submit(function(event) {
  	event.preventDefault();
  	//NEED TO VALIDATE FIELDS
  	$('#eventModal').modal('hide');
  	var name = $('#event_name_input').val();
  	var location = $('#event_location_input').val();
  	var date = $('#event_date_input').val();
  	var startTime = $('#event_start_time_input').val();
  	var endTime = $('#event_end_time_input').val();
	var csrftoken = getCookie('csrftoken');

	if ( dateValidation(date)==false || timeValidation(startTime)==false || 
		timeValidation(endTime)==false || startEndTimeValidation(startTime, endTime) == false ) {
		return false;
	}

  	$.ajaxSetup({
	    beforeSend: function(xhr, settings) {
		    xhr.setRequestHeader("X-CSRFToken", csrftoken);
	    }
	});
  	$.ajax({
  		type: "POST",
		url: "new_event/",
		data: {
			"name": name,
			"location": location,
			"date": date,
			"startTime": startTime,
			"endTime": endTime
		}
	}).done(function() {
		console.log("GOT HERE");
		$( this ).addClass( "done" );
	});
});
