var links = $('.calLink');

/* Change button color when clicked/on that page */
links.click( function() {
	links.removeClass('activeButton');
	$(this).addClass('activeButton');
});

$("#event_date_input").datepicker({ 
	altFormat: "yy-mm-dd",
    dateFormat: "yy-mm-dd",
	onSelect: function(dateText, inst) { 
		$("#datepicker_value").val(dateText); 
	} 
});