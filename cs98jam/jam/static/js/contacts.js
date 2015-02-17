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

$('.contact-export').on('click', function(){
	console.log('BUTTON CLICKED');
	var csrftoken = getCookie('csrftoken');
	console.log("GOT HERE");

	var me = $(this);
	if(me.data('requestRunning')){
		return;
	}
	me.data('requestRunning',true);

	$.ajaxSetup({
	    beforeSend: function(xhr, settings) {
		    xhr.setRequestHeader("X-CSRFToken", csrftoken);
	    }
	});
  	$.ajax({
  		type: "POST",
		url: "/jam/contacts/all/",
		data: {"export": true}
	}).done(function() {
		console.log("GOT HERE");
		me.data('requestRunning',false);
		alert("Check your Downloads folder for a 'jam_contacts.txt' file");
		$( this ).addClass( "done" );
	});
});

var listItem = $('.list-group-item');

listItem.on('click', function(){

	//console.log($(this));

	$(this).addClass('active').siblings().removeClass('active');
	$(this).children('p.list-group-item-text').removeClass('hidden');
	$(this).siblings().children('p.list-group-item-text').addClass('hidden');
});