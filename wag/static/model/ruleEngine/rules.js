//** The rule base **//

	var rules = new Object();
	var xmlns = ' xmlns="http://www.w3.org/1999/xhtml"';

// Image without text alternatives
	rules[1] = function(code) { 				
		var img_arr = Array();
		$(code).find('img:not([alt])').each(function()  {
			var nd = this.outerHTML.replace(xmlns,'');
			img_arr.push(nd);
		});
		return img_arr;
	}
	
// 	Embeded multimedia without noembed (text or audio)
	rules[2] = function(code) { 				
		var video_arr = Array();
		$(code).find('embed').each(function() { 
			var noem = $.trim($(this).children('noembed').text());
			if ( $.isEmptyObject(noem) ) {
				var nd = this.outerHTML.replace(xmlns,''); 
				video_arr.push(nd);
			}
		});
		return video_arr;
	}
	
//	color cues
	rules[3] = function(code) { 				
		var clrcue_arr = Array();
		$(code).find('font[color]').each(function() { 	
				var nd = this.outerHTML.replace(xmlns,''); 
				clrcue_arr.push(nd);
		});	
	
		$(code).find('span[style]').each(function() { //alert($(this).css('color')); //code being xml object doesnt identify css :(
				var nd = this.outerHTML.replace(xmlns,''); 
				clrcue_arr.push(nd);	
		});			
		return clrcue_arr;
	}	

// Table without summary
	rules[4] = function(code) { 
		var tsmary_arr = Array();
		$(code).find('table:not([summary])').each(function() {
			var nd = this.outerHTML.replace(xmlns,'');
			tsmary_arr.push(nd);
		});
		return tsmary_arr;
	}	

// Table without caption
	rules[5] = function(code) { 
		var tcaptn_arr = Array();
		$(code).find('table').each(function() { 
			var cap = $.trim($(this).children('caption').text());
			if ( $.isEmptyObject(cap) ) {
				var nd = this.outerHTML.replace(xmlns,''); 
				tcaptn_arr.push(nd);
			}
		});
		return tcaptn_arr;
	}	
	
//	input elements that need labels
	rules[6] = function(code) { 				
		var lbl_arr = Array();
		$(code).find(':text,:password,:checkbox,:radio,:file,textarea,select').each(function() { 	
			var idVal = $(this).attr('id'); 
			var labl = $(code).find('label[for="'+idVal+'"]').html(); 
			
			if ( !(idVal && labl) ) {
				var nd = this.outerHTML.replace(xmlns,''); 
				lbl_arr.push(nd);
			}
		});		
		return lbl_arr;
	}
	
// 	ondblclick events without onkeypress event
	rules[7] = function(code) { 				
		var dblclk_arr = Array();
		$(code).find('[ondblclick]').each(function() { 
			if ( !($(this).attr('onkeypress')) ) {
				var nd = this.outerHTML.replace(xmlns,'');
				dblclk_arr.push(nd);
			}
		});
		return dblclk_arr;
	}	

// Document without a title
	rules[8] = function(code) { 
		var title_arr = Array();
		var tle = $.trim($(code).find('title').text());
		if ( $.isEmptyObject(tle) ) { 
			title_arr.push('<title>');
		}
		return title_arr;
	}	
	
// Link with bad text (url)
	rules[9] = function(code) { 
		var link_arr = Array();
		$(code).find('a').each(function() { 
			var lnktxt = $.trim($(this).text()); 
			if ( (lnktxt.indexOf("http") != -1) || (lnktxt.indexOf("://www.") != -1) || (lnktxt.indexOf("www") != -1) ) {
				var lnk = this.outerHTML.replace(xmlns,''); 
				link_arr.push(lnk);
			}
		});
		return link_arr;
	}
	
// 	all input elements (include button, textarea ect) and 
//	focusable elements (links, any element with user event ) without tabindex
	rules[10] = function(code) { 				
		var tab_arr = Array();
		$(code).find(':input,a,[onclick],[ondblclick],[onkeydown],[onkeypress]').each(function() { 	
			if ( !($(this).attr('tabindex')) ) {
				var nd = this.outerHTML.replace(xmlns,'');
				tab_arr.push(nd);
			}
		});		
		return tab_arr;
	}	
	

	



