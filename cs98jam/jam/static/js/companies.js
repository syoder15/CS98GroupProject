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

$('.company-export').on('click', function(){
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
		url: "/jam/companies/all/",
		data: {"export": true}
	}).done(function() {
		console.log("GOT HERE");
		$( this ).addClass( "done" );
		me.data('requestRunning',false);
		alert("Check your Downloads folder for a 'jam_companies.txt' file");
	});
});

var listItem = $('.list-group-item');

listItem.on('click', function(){

	console.log($(this));
	var blah = $(this);

	console.log($(this).children());
	console.log($(this).children('p.list-group-item-text'));

	$(this).addClass('active').siblings().removeClass('active');
	$(this).children('p.list-group-item-text').removeClass('hidden');
	$(this).siblings().children('p.list-group-item-text').addClass('hidden');
});



/*$("#company_deadline_input").datepicker({ 
	altFormat: "yy-mm-dd",
    dateFormat: "yy-mm-dd",
	onSelect: function(dateText, inst) { 
		$("#datepicker_value").val(dateText); 
	} 
});*/