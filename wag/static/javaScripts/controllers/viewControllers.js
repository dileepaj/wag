//*** View controller
   	//////////////////////////////////////////////// general //////////////////////////////////////////////
	$(function() { 
			$(".structure").colResizable();
			$(".structure").height($(window).height()-50);
			
			// Buttons
			$( "input:submit, button, input:button", "#dashboard" ).button();
			
			// Tabs
			$('#tabs').tabs();
			
			// List
			$( "#list" ).selectable({
				cancel: 'a'
			});
		
			// Progressbar
			$("#progressbar").progressbar({
				value: 0
			});
			
			// Evaluate button
			$("#eval").click(function() { 
				$( "#dialog-form" ).dialog( "open" );
				$('#eval').attr("disabled", true);
			});
			
			// Apply button
			$("#modify").click(function() {
				var currentUrl = $('#curUrl').text();
				var	curUser = $('#userid').val();
				var source = $('#code').html();
				var tmpDiv = jQuery(document.createElement('div'))
				tmpDiv.html(source.replace(/<br>/g,'\n'))
				var textHtml = tmpDiv.text()
				var oldCode = (textHtml.replace(/&lt/g,"<"));
				
				$.ajax({
                    	url : '/reevaluate',
                    	type : 'POST',
                    	contentType : 'application/json',
                    	data : JSON.stringify(
                    						{
                    							url : currentUrl,
                    							content : oldCode
                    						},
                    						null,
                    						'\t'
                    	),
                    	dataType : 'json',
                    	success : function(data){
                    		updatePageResults(currentUrl, data.evalResults)		
                    	}                    	
                   }); 
			});
		
			// OK button
			$("#ok").click(function() { 
				$('#resolve').hide();
				
				// Select next result
				var id = parseInt($('form').attr('issue'), 10);	
				var next = id + 1;	
				$("#"+next).find("a").click();
			});
			
			// Skip button
			$("#skip").click(function() {
				var r_id = $('form').attr('issue');
				skipViolation(r_id)
			});
			
			// Auto correct button
			$("#autocorct").click(function() {
				var r_id = $('form').attr('issue');
				autoCorrect(r_id);
			});
			
			//PDF download link
			var projectName = $('#siteName').val();
			var downloadLink = "static/reports/WAG_report_"+projectName+".pdf"
			$('#reportDownload').attr("href", downloadLink)
	});
	
	//change status of the violation to skipped
	function skipViolation(index){
		var item = $('#list').find('li[id$='+index+']')
	    var comps =  item.text().split('-');
	    //change status string
	    comps[2] = 'Skipped'
	    item.text(comps.join('-')) 
	    var summary = $('#summary').text()
	    //get the 3rd no in summary string which are the skipped count
	    var amounts = summary.match(/[0-9]/g)
	    var newCount = parseInt(amounts[2])+1
	    $('#summary').html(summary.replace(/Skipped-[0-9]/g, "Skipped-"+newCount))
	    
	    var currentUrl = $('#curUrl').text();
	    $.ajax({
	    	url : '/skip',
	    	type : 'POST',
	    	contentType : 'application/json',
	    	data : JSON.stringify(
	    						{
	    							url : currentUrl,
	    							id  : index	    							
	    						},
	    						null,
	    						'\t'
	    	),
 		 }); 
	}
	
	function checkDisability(type, val){
		$("#disability")
	       .find("input:checkbox")
	       .eq(type).prop("checked", val);
	}
	//////////////////////////////////////////// sourcecode controller /////////////////////////////////////

	function setSrcode(source) { 
		setLine(source);
	
		// replacing lessthans, linebreaks and whitespaces
		var newcode = ((source.replace(/\</g,"&lt")).replace(/\n/g,'<br>')).replace(/ \//g,'/'); 
		$('#code').html(newcode);
		
	}
		
	function modify() {	
		// evaluation after changes
		try{ 
			var plain = (($('#code').html()).replace(/<font style="background-color: lightblue;">/g,'')).replace(/<\/font>/g,''); 
			var cd = ((plain.replace(/\&lt;/g,"<")).replace(/\&gt;/g,">")).replace(/\<br>/g,'\n');
			
			setLine(cd);
			
			scanner.scan(cd);
			list.update(); 
			calcProgress();
			
		} catch(e) {
			alert("Inappropriate source code ! \n");
		}
		
	}
	
	function setLine(code) {
		// setting lines numbers according to the line breaks in the code
		var lines = code.match(/\n/g).length;
		$('#lines').empty();
		for (var i=1; i<lines+3; i++) {
			$('#lines').append(i+'<br>');
		}
	}
	
	function getLine(element) { 
		var srcode = ((($('#code').html()).replace(/\&lt;/g,"<")).replace(/\&gt;/g,">")).replace(/\<br>/g,'\n');
		var e = element.slice(1,-2); 	
		var i = srcode.indexOf(e);				
		
		if (i != -1) {
			var n = srcode.slice(0,i);  
			var count = n.match(/\n/g); 
			var line = count.length;
			return line;
		}		
	}
	
	
	$(function(){
		//var code = JSON.parse($("#code").text());
	 	var code = $("#code").text();
	 	
	 	if (code == ""){
	 		curUrl = $('#curUrl').text();
	 		getSrcode(curUrl)
	 	}else{
	 		setSrcode(code);
	 		retrieveResults()
	 	}
	});
	
	pages = {
      		user : "Anon",
      		siteName : "Default",
			urls : [],
			contents : [],
			disabilities : [],
	        priority : 3
		}
	
	var isInternal = false;
	
	function getSrcode(url){
		
		var siteToanalyze = url;
   		var content = "";
   		var allVals = [];
   		var prio = 1; 	
   		var disabVal = 30;
        if (isValidURL(siteToanalyze)) {
        	
        	$.ajax({
	                url: siteToanalyze,
	                type : 'GET',
	                async : false,
	                success: function (result) {
						if (result.responseText == undefined){
							content = result
							//if sitename is not given, retrieve only one page
							var siteName = $('#siteName').val();
							if (siteName == 'None'){
								analyzeCode(content, siteToanalyze, true)
							}else{
								pages.siteName = siteName;
								analyzeCode(content, siteToanalyze, true)
							}
						}else{
							content = result.responseText;
							pages.siteName = siteName;
							analyzeCode(content, siteToanalyze, false)
						}
						setSrcode(content);
						retrieveResults()
	                },
	                error: function (jqxhr, status, errorThrown) {
	            		jQuery.ajax = oldAjax;
	            		$.ajax({
			                url: siteToanalyze,
			                type : 'GET',
			                success: function (result) {
								content = result
								analyzeCode(content, siteToanalyze, true);
								setSrcode(content);
			        			retrieveResults();
			                },
			                error: function (jqxhr, status, errorThrown) {
			            		alert("Failure, Unable to recieve content");
		            		}
		        		});
            		}
        		});
        } else {
            alert("enter valid URL");
        }
	}
	
	function analyzeCode(content, url, isInternal){
		var allVals = [];
		var prio = 3; 	
		var disabVal = 30;
	    var siteName = $('#siteName').val();
	    pages.user = $('#userid').val()
        pages.siteName = siteName;
	    //The given root page is the first elem in pages collection
		pages.urls.push(url)
		pages.contents.push(content)
		pages.disabilities = ['2','3','5']
		pages.priority = prio
		
		//post page collection in JSON
		if (isInternal)
		 crawl_internal(content, url);
	 	else 
	 	 crawl(content, url);	 
    	var reqType = 'Site'
    	postJson('/pageCollection', pages);
	    
	    $('#reqType').val(reqType)
	}
	
	function isValidURL(url){
    	var RegExp = /(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/;
    	return RegExp.test(url);
	}
	
	function removeDuplis(){
		urls = []
		contents = []
		for (var url in pages.urls){
			if (urls.indexOf(pages.urls[url]) === -1){
				urls.push(pages.urls[url]);
				contents.push(pages.contents[url]);
			}
		}
		
		pages.urls = urls;
		pages.contents = contents;
	}
	
	function crawl_internal(content, parentUrl, first){
		if (first == undefined){
			first = true;
		}
		$(content).find('a').each(function(idx, item){
		var url = (resolveUrl(parentUrl, $(this).attr('href'))).toString();
		if (pages.urls.indexOf(url) == -1){
			if(isValidURL(url)){
				Frame(function(callback){
					childContent = getContent(url, callback);
					crawl(childContent, parentUrl, false);
	    	 });
		    }
       }
       Frame();
	});
	Frame(function(){
	   if(first)
 	  	postJson('/pageCollection', pages);
	});
	Frame.start();
	}
	
	function crawl(content, parentUrl, first){
		if (first == undefined){
			first = true;
		}
		$(content).find('a').each(function(idx, item){
		var url = (resolveUrl(parentUrl, $(this).attr('href'))).toString();
		if (pages.urls.indexOf(url) == -1){
			if(isValidURL(url)){
				Frame(function(callback){
					childContent = getContent(url, callback);
					crawl(childContent, parentUrl, false);
	    	 });
		    }
       }
	});
	Frame(function(){
	   if(first)
 	  	postJson('/pageCollection', pages);
	});
	Frame.start();
	}
	
	function getContent(url, callback){
		var pageContent;
		$.ajax({
	        url: url,
	        type : 'GET',
	        async : false,
	        success: function (result) {
	            if (result.responseText == undefined){
					pageContent = result;
				}else{
					pageContent = result.responseText;
				}
				pages.urls.push(url);
		    	pages.contents.push(pageContent);
		    	callback();
			},
	        error: function (jqxhr, status, errorThrown) {
	            console.log('Failed to retrieve content for' + url)
	        }
	    });
	    return pageContent;
	}
    
    function resolveUrl(parenturl, url){
		var parentUri = new URI(parenturl);
		var childUri = new URI(url);
		var resolvedUri = url 
		if (parentUri.authority == childUri.authority){
			resolvedUri = url
		}else{
			if (isValidURL(url)){
				//If the authorities are different and this is a valid url, then it is assumed as an external link
				//This will not pass the isValidUrl test
				resolvedUri = "External"
			}else{
				resolvedUri = childUri.resolve(parentUri)	
			}
		}
		return resolvedUri
	}
    
	function postJson(posturl, obj){
		$.ajax({
	    	url : posturl,
	    	type : 'POST',
	    	async : false,
	    	contentType : 'application/json',
	    	data : JSON.stringify(obj, null, '\t'),
	    	dataType : 'json'
	    });	
	}
	
	

	function retrieveResults(){
		var curUrl = $('#curUrl').text();
    	var curUser = $('#userid').val();
    	var curName = $('#siteName').val();
    	var evalNum = $('#evalNum').val();
    	var type = $('#reqType').val();
    	
    	if (type == "Page"){
    		console.log(curUrl)
    		getSingleEvalResults(url=curUrl, user = curUser);
    	}
    	
    	if(type == "Site"){
    		console.log(curUrl)
    		getSiteEvalResults(url=curUrl, name=curName, user = curUser, evalNum = evalNum);
    	}	
	}
    function setFilterCriteria(data){
    	var prio = data.priority;
		var disability = data.disability;
		if (disability % 2 != 0){
			checkDisability(0, false)
		}
		if (disability % 3 != 0){
			checkDisability(1, false)
		}
		if (disability % 5 != 0){
			checkDisability(2, false)
		}
	 	$("#priority").val(3);
    }
    
    function highlightNode(code, line, length){
    	lines = code.split("<br>");
    	elemLines = lines.slice(line-1, line+length);
    	return elemLines.join("<br>");	    	
    }
    
    function showDetailsofError(result){
    	
    	$('#resolve').show();
		$('form').attr('issue',result.id);
		
		$('li').removeClass("ui-selected");
		$('#'+result.id+'').addClass("ui-selected");
		$("#des").html(result.ftrInfo.solution+"<br><br>");
		
		$('li').removeClass("ui-selected");
		$('#'+result.id+'').addClass("ui-selected");
		
		//highlight selected violation
		
		var pri = result.ftrInfo.priority;
		var cd = ($('#code').html()).replace(/<font style="background-color: (#FF6633|#FFC200|#66FF33);">|<\/font>/g,'') 
		//alert(cd);
		//var cd = (($('#code').html()).replace(/<font style="background-color: #336633;">/g,'')).replace(/<\/font>/g,''); 
		
		switch(pri)
			{
					case "1":
					var elem = highlightNode(cd, result.line, result.nodeLines);
					var s = cd.replace(elem,'<font style="background-color: #FF6633;">'+elem+'</font>'); 
					$("#code").html(s); 
					break;
					
					case "2":
					//var cd = (($('#code').html()).replace(/<font style="background-color: #336633;">/g,'')).replace(/<\/font>/g,''); 
					var elem = highlightNode(cd, result.line, result.nodeLines);
					var s = cd.replace(elem,'<font style="background-color: #FFC200;">'+elem+'</font>'); 	
					$("#code").html(s); 
					break;
					
					
					case "3":
					var elem = highlightNode(cd, result.line, result.nodeLines);
					var s = cd.replace(elem,'<font style="background-color: #66FF33;">'+elem+'</font>'); 	
					$("#code").html(s); 
					break; 
					
					default:
					var elem = highlightNode(cd, result.line, result.nodeLines);
					var s = cd.replace(elem,'<font style="background-color: #FF6633;">'+elem+'</font>'); 
					$("#code").html(s); 
					break;
			} 
			
			
	/*	var cd = (($('#code').html()).replace(/<font style="background-color: #2F6633;">/g,'')).replace(/<\/font>/g,''); 
		var elem = highlightNode(cd, result.line, result.nodeLines)
		var s = cd.replace(elem,'<font style="background-color: #2F6633;">'+elem+'</font>'); 
		$("#code").html(s); */
		
		var title = result.ftrInfo.title;
		var dis = result.ftrInfo.disability;
		var des = result.ftrInfo.description;
		var sol = result.ftrInfo.solution;
				
		var outMsg = 	"<span class='headings'><h6>Title:</h6> </span><br/><span class='data'>" + title + "</span><br/><br/>" +
						"<span class='headings'><h6>Disability:</h6> </span><br/>" + dis + "<br/><br/>" + 
						"<span class='headings'><h6>Description: </h6></span><br/>" + des + "<br/><br/>" + 
						"<span class='headings'><h6>Solution: </h6></span><br/>" + sol;
			
		$("#feature").html(outMsg);
		
		// scroll to selected violation
		var lineHeight = parseInt($("#wrapper").css('line-height'), 10);
		//$("#wrapper").scrollTop();
		$("#wrapper").scrollTop(result.line*lineHeight);
		
		
    }
    
    function setEvalResults(eval){
    	for(var result in eval){
    		var text = eval[result].ftrInfo.error+' - line '+eval[result].line+' - '+eval[result].status;
		    var jsonRes = JSON.stringify(eval[result])
		    var fn = "showDetailsofError("+jsonRes+"); ";
			var clss = 'ui-widget-content';
			
			switch(eval[result].status)
			{
				case "resolved":
					clss = 'ui-widget-content list-resolved';
					break;
				case "skipped":
					clss = 'ui-widget-content list-skipped';
					break;
				default:
					clss = 'ui-widget-content';
			}
		  
			$('#list').append(
				$('<li>').attr('class',clss).attr('id',eval[result].id).append(
					$('<a>').attr('href','#').attr('onClick',fn).append(text) 
				)
			);	
    	}
    	  
    }
    
    function setSiteResults(eval){
    	var evalResults = eval.evalResults
    	var site = eval.site
    	
    	for (var page in site.pages.urls) {
    		
    		$('#violationTree').append(
    			$('<h4>').attr('class', 'pageUrl accordion-heading').attr('id', 'page' + page).attr('role', 'tab').append(
    				$('<a>').attr('href', 'javascript:void(0)').attr('class', 'accordion-toggle').append(site.pages.urls[page]).on("click", { index : page } , function(obj){
    					contents = site.pages.contents[obj.data.index]
    					$('#curUrl').text(site.pages.urls[obj.data.index])
    					setSrcode(contents)		
    				})
    			)
    		)
    		var viols = $('<div>').attr('class','pageViols accordion-body collapse in').attr('id', site.pages.urls[page]);
    		var results = evalResults[page]
			for (var v in results){
				var text = results[v].ftrInfo.error+' - line '+results[v].line+' - '+results[v].status;
			    var jsonRes = JSON.stringify(results[v])
			    var infn = "showDetailsofError("+jsonRes+"); ";
				var clss = 'ui-widget-content';
				
				switch(results[v].status)
				{
					case "resolved":
						clss = 'ui-widget-content list-resolved violations-list';
						break;
					case "skipped":
						clss = 'ui-widget-content list-skipped violations-list';
						break;
					default:
						clss = 'ui-widget-content violations-list';
				}
			
	   			viols.append(
					$('<li>').attr('class',clss).attr('id',results[v].id).append(
					$('<a>').attr('href','javascript:void(0)').attr('class','black').attr('onClick',infn).append(text) 
					)
				)
			}
			$('#violationTree').attr('class', 'accordion').append(viols)
    	}
    	
    	$('#violationTree').accordion({
			collapsible : true,
			heightStyle :"content"
		});
		
		var firstContents = site.pages.contents[0]
		$('#curUrl').text(site.pages.urls[0])
		setSrcode(firstContents)	
    }
    
    function updatePageResults(curUrl, results){
    	var urlTab = $('#violationTree').find('h4:contains('+ curUrl + ')');
    	var violsDiv = urlTab.next()
    	violsDiv.empty()
    	for (var v in results){
			var text = results[v].ftrInfo.error+' - line '+results[v].line+' - '+results[v].status;
		    var jsonRes = JSON.stringify(results[v])
		    var infn = "showDetailsofError("+jsonRes+"); ";
			var clss = 'ui-widget-content';
			
			switch(results[v].status)
			{
				case "resolved":
					clss = 'ui-widget-content list-resolved';
					break;
				case "skipped":
					clss = 'ui-widget-content list-skipped';
					break;
				default:
					clss = 'ui-widget-content';
			}
		
   			violsDiv.append(
				$('<li>').attr('class',clss).attr('id',results[v].id).append(
				$('<a>').attr('href','#').attr('onClick',infn).append(text) 
				)
			)
		}        
    }
    
    function calcProgress(progress){
    	var prsntg = (progress.resolves/progress.total)*100; 
		$("#progressbar").progressbar({value: prsntg});
		$("#summary").html("Summary: &nbsp;&nbsp;&nbsp;&nbsp; Total-"+progress.total+" &nbsp;&nbsp;&nbsp;&nbsp; Resolved-"+progress.resolves+" &nbsp;&nbsp;&nbsp;&nbsp; Skipped-"+progress.skips);
		$("#p").html(Math.round(prsntg*Math.pow(10,2))/Math.pow(10,2)+" %");
    }
    
    function getSingleEvalResults(pageurl, user){
    	$.ajax({
    		url : '/resultsPage',
    		contentType : 'application/json',
    		data : JSON.stringify(
    			{
    				url: pageurl    				
    			},
    			null,
    			'\t'
    		),
            type : 'POST',
            dataType : 'json',
            async : false,
	    	success : function(data){
	    		setEvalResults(data.evalResults)
			}
    	});
    	
    }
    
    function getSiteEvalResults(home, name, user, evalNum){
    	$.ajax({
    		url : '/resultsSite',
            type : 'POST',
            contentType : 'application/json',
      		data : JSON.stringify(
    			{
    				url: home,
    				siteName : name,
    				evalNum : evalNum,
    				username : user     				
    			},
    			null,
    			'\t'
    		),
            dataType : 'json',
            async : false,
	    	success : function(data){
	    		setSiteResults(data.siteResults)
			}
    	});
    }
