var contactForm = $('.contact_form');
var companyForm = $('.company_form');
var eventForm = $('.event_form');
var channelForm = $('.channel_form');

// change the site for absolute URL paths depending on whether we're in development 
// vs. production environment.
var localTest = true; 
var site = "http://dartmouthjam.pythonanywhere.com/jam/"
if(localTest){
	site = "http://127.0.0.1:8000/jam/";
}


// JS functions necessary for modal form validation
// real-time inline error validation is a-go!


//validating company form fields
function validateDeadline(deadline_id){
	var deadline = $('#' + deadline_id).val();
	//var deadline = $('#company_deadline_input').val();
	var msg = dateValidation(deadline);
	if(msg != true){
		$('.error-message').show();
		$('#' + deadline_id).css('border','solid 2px red');
		$('.error-message').html(msg);
		console.log("DATE ERROR " + deadline)
	}
	else{
		$('.error-message').hide();
		$('#' + deadline_id).css('border','solid 0px red');
	}
	return msg;
}

function validateTimes(start_id, end_id){
	console.log("validateTimes");
	var start = $('#' + start_id).val();
	var end = $('#' + end_id).val();
	var msg = startEndTimeValidation(start, end);
	if(msg != true){
		$('.time-error').show();
		$('#' + end_id).css('border','solid 2px red');
		$('.time-error').html(msg);
	}
	else{
		$('.time-error').hide();
		$('#' + end_id).css('border','solid 0px red');
	}
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

$('.channel-btn').on('click', submitChannelForm);
function submitChannelForm(event){
	if (validateName('channel_name_input') != '' || validateName('moniker_input') != '' || validateName('description_input') !=''){
		return false;
	}
	event.preventDefault();
	var me = $(this);
	me.off('click');
	if(me.data('requestRunning')){
		return;
	}
	me.data('requestRunning',true);

	var name = $('#channel_name_input').val();
	var moniker = $('#moniker_input').val();
	var description = $('#description_input').val();
	var category = $('#category_input').val();
	var is_public = $('#is_public_input').val();
	var csrftoken = getCookie('csrftoken');

	var donezo = true;

	$.ajaxSetup({
	    beforeSend: function(xhr, settings) {
		    xhr.setRequestHeader("X-CSRFToken", csrftoken);
	    }
	});
  	$.ajax({
  		type: "POST",
  		cache:false,
		url: site + "channels/create/",
		data: {
			"name": name,
			"moniker": moniker,
			"description": description,
			"category_names": category,
			"is_public":is_public
		},
		success: function(){
			donezo = true;
			$('.server-error').hide();
			$('#channelModal').modal('hide');
			$('input').val('');
			$('textarea').val('');
		},

		//handles error response
		error: function(response){
			console.log('got to error sadly');
			me.on('click', submitChannelForm);
			me.data('requestRunning',false);
			var errors = JSON.parse(response.responseText);
			for(error in errors){
				$('.server-error').html(errors[error]);
			}
			console.log('about to return false');
			return false;
		}
	}).done(function() {
		if(donezo){
			console.log("GOT HERE");
			$( this ).addClass( "done" );
			me.on('click', submitChannelForm);
			location.reload();
		}
	});
};



$('.contact-btn').on('click', submitContactForm);
function submitContactForm(event){
	
	// if there are any client-side errors apparent, do NOT go through AJAX validation
	if(validateEmailAddress() !='' || validatePhone() !='' || validateName('name_input') != '' || validateName('company_input') != ''){
		return false;
	}

  	event.preventDefault();
  	var me = $(this);
	me.off('click');

	if( me.data('requestRunning')){
		return;
	}
	me.data('requestRunning', true);

  	//$("input[type=submit]").attr("disabled", "disabled");

  	//NEED TO VALIDATE FIELDS
  	var name = $('#name_input').val();
  	var phone = $('#phone_number_input').val();
  	var email = $('#email_input').val();
  	var company = $('#company_input').val();
  	var notes = $('#comment').val();
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
		url: site + "new_contact/",
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
			console.log('got to error sadly');
			//$("input[type=submit]").attr("disabled", false);
			me.on('click', submitContactForm);
			me.data('requestRunning',false);
			var errors = JSON.parse(response.responseText);
			for(error in errors){
				$('.server-error').html(errors[error]);
			}
			console.log('about to return false');
			return false;
		}
	}).done(function() {
		//
		if(donezo){
			console.log("GOT HERE");
			$( this ).addClass( "done" );
			me.on('click', submitContactForm);
			location.reload();
		}
	});
};

//var xhr = undefined;
$('.company-btn').on('click', submitCompanyForm);

//companyForm.submit(function(event){
	//disable button during a submit to prevent double submission

function submitCompanyForm(event){	
	//UPLOAD MULTIPLE
	/*
	console.log("submitting companyForm");
	var file = $('#id_filep');
	if (file.val()){
		console.log("file has value");
		companyForm.submit();
		//return;
	}
	*/
	console.log("IN SUBMIT COMPANY");
	event.preventDefault();
	var file = $('#id_filep');
	console.log("FILE = " + file.val());
	if(file.val()){
		console.log('file has value');
		//companyForm.submit();
	}

	var me = $(this);
	me.off('click');

	if( me.data('requestRunning')){
		return;
	}

	me.data('requestRunning', true);
	
	
	// if there are any client-side errors apparent, do NOT go through AJAX validation
	if (validateDeadline('company_deadline_input') != true || validateName('company_name_input') != ""){
		console.log("GOT TO THIS PART");
		me.on('click', submitCompanyForm);
		me.data('requestRunning', false);
		return false;
	}

	//$("input[type=submit]").attr("disabled", "disabled");

	// if(typeof(xhr)!='undefined'){
	// 	xhr.abort();
	// 	xhr = undefined;
	// }
	
  	//NEED TO VALIDATE FIELDS
  	var name = $('#company_name_input').val();
  	var deadline = $('#company_deadline_input').val();
  	var company_notes = $('#comment').val();
  	var app_link = $('#company_app_link').val();
	var csrftoken = getCookie('csrftoken');

	var formName = $('.company_form').attr('name');

	var donezo = false;
	console.log("GOT HERE");
  	// xhr = 

  	$.ajaxSetup({
	    beforeSend: function(xhr, settings) {
		    xhr.setRequestHeader("X-CSRFToken", csrftoken);
	    }
	});
  	$.ajax({
  		type: "POST",
  		cache:false,
		url: site + "new_company/",
		data: {
			"name": name,
			"deadline": deadline,
			"company_notes": company_notes,
			"app_link": app_link
		},
		singleton:true,
        delay:500,
        blocking:true,
		success: function(){
			donezo = true;
			console.log("SUCCESS")
			$('.server-error').hide();
			$('#companyModal').modal('hide');
			$('input').val('');
			$('textarea').val('');
			//$("input[type=submit]").prop("disabled", false);
			//xhr = undefined;
		},

		//handles error response
		error: function(response){
			//console.log(response);
			console.log("ERRORERROR" + name)
			//$("input[type=submit]").prop("disabled", false);
			var errors = JSON.parse(response.responseText);
			for(error in errors){
				$('.server-error').html(errors[error]);
			}
			me.on('click', submitCompanyForm);
			me.data('requestRunning',false);
			//xhr = undefined;
			return false;

		}
	}).done(function() {
		//
		if(donezo){
			me.on('click', submitCompanyForm);
			//$("input[type=submit]").prop("disabled", false);
			console.log("GOT HERE");
			$( this ).addClass( "done" );
			location.reload();
		}
		else{
			return false;
		}
	});
};

$('.event-btn').on('click', submitEventForm);

function submitEventForm(event){	
	event.preventDefault();
	var me = $(this);
	me.off('click');

	if( me.data('requestRunning')){
		return;
	}

	me.data('requestRunning', true);
	// if there are any client-side errors apparent, do NOT go through AJAX validation
	if (validateName('event_name_input') != ""){
		me.on('click', submitEventForm);
		me.data('requestRunning',false);
		return false;
	}
	
  	var name = $('#event_name_input').val();
  	console.log(name);
  	var type = $('#event_type_input').val();
  	console.log(type);

  	var date = $('#event_date_input').val();
  	var description = $('#event_description_input').val();
  	var companies = $('#event_companies_input').val();
  	var startTime = $('#event_start_time_input').val();
  	console.log("START" + startTime);
  	var endTime = $('#event_end_time_input').val();
  	console.log("END" + endTime);
  	var recurrence = $('#event_recurrence_input').val();
	var channel = $('#channel_input').val();
	var csrftoken = getCookie('csrftoken');

	if ( dateValidation(date)!=true || timeValidation(startTime)==false || 
		timeValidation(endTime)==false || startEndTimeValidation(startTime, endTime) !=true ) {
		me.on('click', submitEventForm);
		me.data('requestRunning',false);
		return false;
	}

	var formName = $('.event_form').attr('name');

	var donezo = false;

  	$.ajaxSetup({
	    beforeSend: function(xhr, settings) {
		    xhr.setRequestHeader("X-CSRFToken", csrftoken);
	    }
	});
  	$.ajax({
  		type: "POST",
  		cache:false,
		url: site + "new_event/",
		data: {
			"name": name,
			"description": description,
			"companies": companies,
			"event_type": type,
			"event_date": date,
			"start_time": startTime,
			"end_time": endTime,
			"recurrence": recurrence,
			"channel": channel
		},
		singleton:true,
        delay:500,
        blocking:true,
		success: function(){
			donezo = true;
			console.log("SUCCESS")
			$('.server-error').hide();
			$('#eventModal').modal('hide');
			$('input').val('');
			$('textarea').val('');
		},

		//handles error response
		error: function(response){
			//console.log(response);
			console.log("ERRORERROR" + name);
			//$("input[type=submit]").prop("disabled", false);
			var errors = JSON.parse(response.responseText);
			for(error in errors){
				$('.server-error').html(errors[error]);
			}
			me.on('click', submitEventForm);
			me.data('requestRunning',false);
			return false;

		}
	}).done(function() {
		//
		if(donezo){
			me.on('click', submitEventForm);
			//$("input[type=submit]").prop("disabled", false);
			console.log("GOT HERE");
			$( this ).addClass( "done" );
			location.reload();
		}
		else{
			return false;
		}
	});
};
