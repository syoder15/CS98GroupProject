var addContact = $('.addcontact');
var addCompany = $('.addcompany');;
var addEvent = $('.addevent');;
var profileDropDown = $('.profileNameButton');
var contactForm = $('.contact_form');
var companyForm = $('.company_form');
var eventForm = $('.event_form');
var uploadFileButton = $('.upload-file');

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

contactForm.submit(function(event) {
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
