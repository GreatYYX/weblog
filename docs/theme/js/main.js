$(document).ready(function(){
	// console.log('main.js');

	/* highlight js */
	hljs.configure({tabReplace: '    '});
	$('pre').each(function(i, block){
		hljs.highlightBlock(block);
	});

	/* about page */
	var about_btn_cn = $('#lang-btn-cn');
	var about_section_cn = $('section#content #lang-cn');
	var about_btn_en = $('#lang-btn-en');
	var about_section_en = $('section#content #lang-en');
	about_btn_cn.click(function(){
		if (!about_btn_cn.hasClass('lang-btn-active')) {
			// inactivate en
	    	about_btn_en.addClass('lang-btn-hover');
	    	about_btn_en.removeClass('lang-btn-active');
	    	about_section_en.addClass('lang-section-hide');
	    	// activate cn
	    	about_btn_cn.addClass('lang-btn-active');
	    	about_section_cn.removeClass('lang-section-hide');
	    }
	});
	about_btn_en.click(function(){
		if (!about_btn_en.hasClass('lang-btn-active')) {
			// inactivate cn
	    	about_btn_cn.addClass('lang-btn-hover');
	    	about_btn_cn.removeClass('lang-btn-active');
	    	about_section_cn.addClass('lang-section-hide');
	    	// activate en
	    	about_btn_en.addClass('lang-btn-active');
	    	about_section_en.removeClass('lang-section-hide');
	    }
	});

});