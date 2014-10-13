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