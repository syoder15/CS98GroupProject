var addContact = document.getElementById('addcontact');
var addCompany = document.getElementById('addcompany');
var addEvent = document.getElementById('addevent');

addContact.addEventListener('click', function(){
	var overlay = document.getElementById('overlay');
	overlay.style.display = "block";
    console.log("This will create a contact!");
});

addCompany.addEventListener('click', function(){
    console.log("This will create a company!");
});

addEvent.addEventListener('click', function(){
    console.log("This will create an event!");
});
