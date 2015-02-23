var links = $('.calLink');

/* Change button color when clicked/on that page */
links.click( function() {
	links.removeClass('activeButton');
	$(this).addClass('activeButton');
});

$("#end_date_div").hide();

$("#event_date_input").datepicker({ 
	altFormat: "yy-mm-dd",
    dateFormat: "yy-mm-dd",
	onSelect: function(dateText, inst) { 
		$("#datepicker_value").val(dateText); 
	} 
});

$("#end_date_input").datepicker({ 
	altFormat: "yy-mm-dd",
    dateFormat: "yy-mm-dd",
	onSelect: function(dateText, inst) { 
		$("#datepicker_value").val(dateText); 
	} 
});

$(document).ready(function(){
    $('#event_recurrence_input').on('change', function() {
      if ( this.value != 'None')
      { 
        $("#end_date_div").show();
      }     
        else
      { 
        $("#end_date_div").hide();
     }
    })
});