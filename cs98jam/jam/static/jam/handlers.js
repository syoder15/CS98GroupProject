var addContact = document.getElementById('addcontact');
var addCompany = document.getElementById('addcompany');
var addEvent = document.getElementById('addevent');

addContact.addEventListener('click', function(){
	var contactOverlay = document.getElementById('contact_overlay');
	contactOverlay.style.display = "block";
    console.log("This will create a contact!");
});

addCompany.addEventListener('click', function(){
	var companyOverlay = document.getElementById('company_overlay')
	companyOverlay.style.display = "block";
    console.log("This will create a company!");
});

addEvent.addEventListener('click', function(){
	var eventOverlay = document.getElementById('event_overlay')
	eventOverlay.style.display = "block";
    console.log("This will create an event!");
});
