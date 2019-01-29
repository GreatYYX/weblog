$(document).ready(function(){
	// console.log('main.js');

	/* highlight js */
	hljs.configure({tabReplace: '    '});
	$('pre').each(function(i, block){
		hljs.highlightBlock(block);
	});

	/* image caption */
	$('img[title]').each(function(i, block){
		$('<div class="image-caption">' + $(this).attr('title') + '</div>').insertAfter($(this));
	});

	/* external link */
	var host = new RegExp('/' + window.location.host + '/');
	$('article section#content a').each(function() {
		if(!host.test(this.href) && !$(this).attr('target')) {
			$(this).attr('target', '_blank');
			$(this).append('<i class="fa fa-external-link-square yyx-external-link"></i>');
		}
	});

	/* nav expansion */
	$('#nav-expand-btn').click(function() {
		$('#header-menu ul').toggleClass('header-nav-show-small');
	});

});