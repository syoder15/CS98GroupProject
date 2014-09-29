var addContact = $('.addcontact');
var addCompany = $('.addcompany');;
var addEvent = $('.addevent');;
var contactForm = document.getElementById('contact_form');

addContact.on('click', function(){
	var contactOverlay = document.getElementById('contact_overlay');
	contactOverlay.style.display = "block";
    console.log("This will create a contact!");
});

addCompany.on('click', function(){
	var companyOverlay = document.getElementById('company_overlay')
	companyOverlay.style.display = "block";
    console.log("This will create a company!");
});

addEvent.on('click', function(){
	var eventOverlay = document.getElementById('event_overlay')
	eventOverlay.style.display = "block";
    console.log("This will create an event!");
});

// contactForm.submit(function(event) {
// 	debugger;
//   	event.preventDefault();
//   	console.log("The form has been submitted");
// });
