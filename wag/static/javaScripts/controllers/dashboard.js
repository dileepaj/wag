//*** controllers for dashboard elements
   	//////////////////////////////////////////////// general //////////////////////////////////////////////
google.load('visualization', '1', { 'packages': ['annotatedtimeline'] });
google.setOnLoadCallback(function(){
	$(function() {
		var	curUser = $('#userid').val();
	   $("#history").click(function(){
	   		$.ajax({
	   			url : '/projectHistory',
	            type : 'POST',
	            contentType : 'application/json',
	      		data : JSON.stringify(
	    			{
	    				home : 'ALSI'    				
	    			},
	    			null,
	    			'\t'
	    		),
	            dataType : 'json',
	            async : false,
		    	success : function(data){
		    		populateGraph(data.result)
				}   		
			});
	   });
	
	   $("#dashbrd").click(function(){
	   	fillProjectsTable();
	   });
       		
	   //Initially fill the projects table on page load. 
	   fillProjectsTable();
	   
	   //Re-Evaluate button click event
	   $(document).on("click",'.resubmit', function(){
	   		var rowId = $(this).attr("id")
	   		var rowNum = parseInt(rowId.substr(rowId.length - 1))
	   		url = $('table#projects tr').eq(rowNum+1).find('td:eq(1) a').text()
	   		name = $('table#projects tr').eq(rowNum+1).find('td:eq(0) a').text()
	   		reSubmit(name, url)
	   });
	   
	});
});

function initSubmit(){
	url = $("#externURL").val();
	getSrcCode(url, init=true)
}

function reSubmit(name, url){
	getSrcCode(url, init = false, siteName = name)
}


function getSrcCode(url, init, siteName){
	if (siteName == undefined){
		siteName = 'Default'
	}
  	pages.siteName = siteName
  	var siteToanalyze = url
	var content = "";
	if (isValidURL(siteToanalyze)) {
    	$.ajax({
            url: siteToanalyze,
            type : 'GET',
            success: function (result) {
            	if (result.responseText == undefined){
					content = result
					if (init){
	    				analyzeCode(content, siteToanalyze, init, true)
	        		}else{
	        			reanalyzeCode(content, siteToanalyze, init, true)
        			}
				}else{
					content = result.responseText;
					if (init){
	    				analyzeCode(content, siteToanalyze, init, false)
	        		}else{
	        			reanalyzeCode(content, siteToanalyze, init, false)		
					}               		
        			content = result;
    			}                	
            },
            error: function (jqxhr, status, errorThrown) {
                jQuery.ajax = oldAjax;
                isInternal = true;
        		$.ajax({
	                url: siteToanalyze,
	                type : 'GET',
	                success: function (result) {
						content = result
						if (init){
		    				analyzeCode(content, siteToanalyze, init, true)
		        		}else{
		        			reanalyzeCode(content, siteToanalyze, init, true)
	        			}
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
    
	var prio = $('#priority').val();
    $('#disability :checked').each(function () {
        allVals.push($(this).val());
    });
    var total = 1;
    for (var v in allVals){
    	total = total * v
    }
    disabVal = total;
    
    pages.user = $('#userid').val()
    pages.siteName = $('#projName').val()
    console.log(pages.user)
    //The given root page is the first elem in pages collection
	pages.urls.push(url)
	pages.contents.push(content)
	pages.disabilities = allVals
	pages.priority = prio
    $.blockUI({message : '<h1><img src="static/img/ajax-loader.gif" /> Crawling your web site... </h1>'})
	if (isInternal)
		crawl_internal(content, url, true);
	else 
		crawl(content, url, true);
}

function reanalyzeCode(content, url, init, isInternal){
	pages.user = $('#userid').val()
    pages.urls.push(url)
	pages.contents.push(content)
	$.blockUI({message : '<h1><img src="static/img/ajax-loader.gif" /> Crawling your web site... </h1>'})
	if(isInternal)
	 crawl_internal(content, url, false);
	else
	 crawl(content, url, false);
	 	
//	postData(content, url, init)
}

//Need a test for localhost connection
function isValidURL(url){
	
    var RegExp = /(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/;
    var isValid = RegExp.test(url); 
    return isValid;
} 

//stores the descendant urls of the submitted url
pages = {
      		user : "Guest",
      		siteName : "Default",
			urls : [],
			contents : [], 
			disabilities : ['2', '3' , '5'],
			priority : 3
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

function crawl(content, parentUrl, init, first){
	if (first == undefined){
		first = true;
	}
	
	$(content).find('a').each(function(idx, item){
		var url = (resolveUrl(parentUrl, $(this).attr('href'))).toString();
		if (pages.urls.indexOf(url) == -1){
			if(isValidURL(url)){
				Frame(function(callback){
					childContent = getContent(url, callback);
					crawl(childContent, parentUrl, init, false);
	    	 });
		    }
       }
   	});
	Frame(function(){
	   if(first)
 	  	postData(content, parentUrl, init)
	});
	Frame.start();
}

function crawl_internal(content, parentUrl, init, first){
	if (first == undefined){
		first = true;
	}
	
	$(content).find('a').each(function(idx, item){
		var url = (resolveUrl(parentUrl, $(this).attr('href'))).toString();
		if (pages.urls.indexOf(url) == -1){
			if(isValidURL(url)){
				Frame(function(callback){
					childContent = getContent(url, callback);
					crawl(childContent, parentUrl, init, false);
	    	 });
		    }
       }
   	Frame();
	});
	Frame(function(){
	   if(first)
 	  	postData(content, parentUrl, init)
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

function postData(content, url, init){
    removeDuplis();
    if(init){
		var allVals = [];
		var prio = 3; 	
		var disabVal = 30;
	    
		var prio = $('#priority').val();
	    $('#disability :checked').each(function () {
	        allVals.push($(this).val());
	    });
	    var total = 1;
	    for (var v in allVals){
	    	total = total * v
	    }
	    disabVal = total;
	    
		postJson('/pageCollection', pages);
		$.unblockUI();
	    postToUrl('/submitPage', {'content' : content,
	    						  'url' : url,
	    						  'disabilities' : disabVal,
	    						  'reqType' : 'Site',
	    						  'siteName' : pages.siteName,
	    						  'priority' : prio}, asJson = false);
	}else{
		postJson('/pageCollection', pages);
	    $.unblockUI();
	    postToUrl('/resubmitPage', {'content' : content,
	    						  'url' : url,
	    						  'reqType' : 'Site',
	    						  'siteName' : pages.siteName}, asJson = false);
	}
}
//Creates a form post
function postToUrl(path, data, asJson){
	method = "post"	

	if (asJson){
		postJson('/json/submitPage', data)
	}
	else {
		var form = document.createElement("form");
		form.setAttribute("method", method);
		form.setAttribute("action", path)
		
		for (var key in data)	{
			if (data.hasOwnProperty(key)){
				var hidden = document.createElement("input");
				hidden.setAttribute("type", "hidden");
				hidden.setAttribute("name", key);
				hidden.setAttribute("value", data[key]);
				
				form.appendChild(hidden);	
			}
		}
		
		document.body.appendChild(form)
		form.submit();
	} 
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


function populateGraph(histData){
    var data = new google.visualization.DataTable();
    data.addColumn('date', 'Date');
    data.addColumn('number', 'Number of lines');
    data.addColumn('string', 'Error type');
    data.addColumn('string', 'Error details');
    data.addColumn('number', 'Number of errors');
    data.addColumn('string', 'Status');
    data.addColumn('string', 'text2');
    data.addRows([
      [new Date(2013, 1, 1), 30000, undefined, undefined, 40645, undefined, undefined],
      [new Date(2013, 1, 2), 14045, undefined, undefined, 20374, undefined, undefined],
      [new Date(2013, 1, 3), 55022, undefined, undefined, 50766, undefined, undefined],
      [new Date(2013, 1, 4), 55022, undefined, undefined, 50766, undefined, undefined],
      [new Date(2013, 1, 4), 75284, undefined, undefined, 14334, 'Not yet completed', 'New error noted'],
      [new Date(2013, 1, 5), 41476, 'Picture tag', 'Picture does not have a tag', 66467, 'Not yet completed', 'New error noted'],
      [new Date(2013, 1, 6), 33322, undefined, undefined, 39463, undefined, undefined]
    ]);

	var projData = new google.visualization.DataTable();
	projData.addColumn('date', 'Evaluated Time');
	projData.addColumn('number', 'Number of Violations')
	for (var i in histData){
		projData.addRows([
		[new Date(histData[i].time.year, histData[i].time.month, histData[i].time.day, histData[i].time.hour, histData[i].time.minute),
		histData[i].total]
	])	
	}
	
	var chart = new google.visualization.AnnotatedTimeLine(document.getElementById('chart_div'));
    chart.draw(projData, { displayAnnotations: true });
}

function fillProjectsTable(curUser){
	$.ajax({
        	url : '/projectList',
        	type : 'POST',
        	contentType : 'application/json',
        	data : JSON.stringify(
        						{
        							user : curUser, 
        						},
        						null,
        						'\t'
        	),
        	dataType : 'json',
        	success : function(data){
        		var sites = data.siteList;
        		for (var i in sites){
					var row = $('<tr></tr>');
					row.append($('<td>').html( '<a href="project?site='+sites[i].name+'" >' +sites[i].name+'</a>'));
					//have to check user in session from server
					row.append($('<td>').html( '<a href="loadEval?site='+sites[i].name+'&url='+sites[i].homeUrl+'" >' +sites[i].homeUrl+'</a>'));
					row.append($('<td>').text(sites[i].LastEvalTime));
					row.append($('<td class="center-txt">').text(sites[i].violationCount));
					if (sites[i].status == "cool"){
						row.append($('<td class="center-txt">').html('<img src="static/img/green_light.png" width="20%" height="5%" alt="statusOK">'));
					}
					if (sites[i].status == "uncool"){
						row.append($('<td class="center-txt">').html('<img src="static/img/red_light.png" width="20%" alt="statusOK">'));
					}
					row.append($('<td>').append($('<a href="javascript:void(0)" class="resubmit btn btn-danger btn-small2" id="site'+i+'">Re-evaluate</a>')));
					$('#projects').append(row);
				}		
        	}                    	
       });
}
