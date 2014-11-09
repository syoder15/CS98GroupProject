var links = $('.calLink');

/* Change button color when clicked/on that page */
links.click( function() {
	links.removeClass('activeButton');
	$(this).addClass('activeButton');
});