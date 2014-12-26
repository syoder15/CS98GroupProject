var contactForm = $('.contact_form');
var companyForm = $('.company_form');
var eventForm = $('.event_form');

// JS functions necessary for modal form validation
// real-time inline error validation is a-go!


//validating company form fields
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

function validateName(input){
	var name = $('#'+input).val();
	error_element = $('[name="' + input + '"]');

	if(name.length === 0){
		// add the error message, show it!
		error_element.html('Please fill out this field!');
		error_element.show();

		// add the red highlight and return an error
		$('#' + input).css('border','solid 2px red');
		return 'error';
	}
	else{		
		error_element.hide();
		$('#' + input).css('border','solid 0px red');
		return '';
	}
}

// validating contact fields

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


/*
functions to validate form before submitting. 
forms will not submit until all errors can be seen to be cleared!
*/
contactForm.submit(function(event){
	
	// if there are any client-side errors apparent, do NOT go through AJAX validation
	if(validateEmailAddress() !='' || validatePhone() !='' || validateName('name_input') != '' || validateName('company_input') != ''){
		return false;
	}


  	event.preventDefault();
  	//NEED TO VALIDATE FIELDS
  	var name = $('#name_input').val();
  	var phone = $('#phone_number_input').val();
  	var email = $('#email_input').val();
  	var company = $('#company_input').val();
  	var notes = $('#contact_notes_input').val();
	var csrftoken = getCookie('csrftoken');

	var formName = $('.contact_form').attr('name');

	var donezo = false;

  	$.ajaxSetup({
	    beforeSend: function(xhr, settings) {
		    xhr.setRequestHeader("X-CSRFToken", csrftoken);
	    }
	});
  	$.ajax({
  		type: "POST",
  		cache:false,
		url: "new_contact/",
		data: {
			"name": name,
			"phone": phone,
			"email": email,
			"company": company,
			"notes":notes
		},
		success: function(){
			donezo = true;
			$('.server-error').hide();
			$('#contactModal').modal('hide');
			$('input').val('');
			$('textarea').val('');
		},

		//handles error response
		error: function(response){
			//console.log(response);

			var errors = JSON.parse(response.responseText);
			for(error in errors){
				$('.server-error').html(errors[error]);
			}
			return false;
		}
	}).done(function() {
		//
		if(donezo){
			console.log("GOT HERE");
			$( this ).addClass( "done" );
			location.reload();
		}
	});
});

var xhr = undefined;

companyForm.submit(function(event){
	//disable button during a submit to prevent double submission

	
	event.preventDefault();

	// if there are any client-side errors apparent, do NOT go through AJAX validation
	if (validateDeadline() != "" || validateName('company_name_input') != ""){
		return false;
	}

	//$("input[type=submit]").attr("disabled", "disabled");

	if(typeof(xhr)!='undefined'){
		xhr.abort();
		xhr = undefined;
	}
  	//NEED TO VALIDATE FIELDS
  	var name = $('#company_name_input').val();
  	var deadline = $('#company_deadline_input').val();
  	var company_notes = $('#company_notes_input').val();
	var csrftoken = getCookie('csrftoken');

	var formName = $('.company_form').attr('name');

	var donezo = false;

  	xhr = $.ajaxSetup({
	    beforeSend: function(xhr, settings) {
		    xhr.setRequestHeader("X-CSRFToken", csrftoken);
	    }
	});
  	$.ajax({
  		type: "POST",
  		cache:false,
		url: "new_company/",
		data: {
			"name": name,
			"deadline": deadline,
			"company_notes": company_notes
		},
		singleton:true,
        delay:500,
        blocking:true,
		success: function(){
			donezo = true;
			$('.server-error').hide();
			$('#companyModal').modal('hide');
			$('input').val('');
			$('textarea').val('');
			$("input[type=submit]").prop("disabled", false);
			xhr = undefined;
		},

		//handles error response
		error: function(response){
			//console.log(response);
			$("input[type=submit]").prop("disabled", false);
			var errors = JSON.parse(response.responseText);
			for(error in errors){
				$('.server-error').html(errors[error]);
			}
			xhr = undefined;
			return false;

		}
	}).done(function() {
		//
		if(donezo){
			$("input[type=submit]").prop("disabled", false);
			console.log("GOT HERE");
			$( this ).addClass( "done" );
			location.reload();
		}
		else{
			return false;
		}
	});
});
