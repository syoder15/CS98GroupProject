var contactInfo = $('.contactInfo');


contactInfo.submit(function(event) {
  	event.preventDefault();
  	//NEED TO VALIDATE FIELDS
  	// var firstName = $('#first_name_input').val();
  	// var lastName = $('#last_name_input').val();
  	// var email = $('#email_input').val();
  	// var phone = $('#phone_number_input').val();
  	// var street = $('#street_input').val();
  	// var city = $('#city_input').val();
  	// var state = $('#state_input').val();
  	// var zipCode = $('#zip_input').val();

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
	var csrftoken = getCookie('csrftoken');

  	$.ajaxSetup({
	    beforeSend: function(xhr, settings) {
		    xhr.setRequestHeader("X-CSRFToken", csrftoken);
	    }
	});
  	$.ajax({
  		type: "POST",
		url: "profile/new_profile/",
		data: {
			"first_name": firstName,
			"last_name": lastName,
			"phone": phone,
			"email": email,
			"phone": phone,
			"address": street,
			"city": city,
			"state": state,
			"zip_code": zipCode
			"gender": gender
		}
	}).done(function() {
		console.log("GOT HERE");
		$( this ).addClass( "done" );
	});
});
