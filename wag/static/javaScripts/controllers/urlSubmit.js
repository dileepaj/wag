//** View Controller

////////////////////////////////////////////URL submission/////////////////////////////////////////////////////////////

$(function () {

$("#externURL").keypress(function(e){
    if(e.keyCode == 13){
             $("#URLSubmit").click()
    }
     })

    $("#URLSubmit").click(function () {
      	pages = {
      		user : "Anon",
      		siteName : "Default",
			urls : [],
			contents : [],
			disabilities : [],
	        priority : 1
		}
      	var siteToanalyze = $("#externURL").val();
   		var content = "";
   		var allVals = [];
   		var prio = 1; 	
   		var disabVal = 30;
        if (isValidURL(siteToanalyze)) {
        	
        	$.ajax({
	                url: siteToanalyze,
	                type : 'GET',
	                success: function (result) {
						if (result.responseText == undefined){
							content = result
							analyzeCode(content, siteToanalyze, pages, 'Page')
						}else{
							content = result.responseText;
							analyzeCode(content, siteToanalyze, pages, 'Page')		
						}               		
                		content = result;
						   
	                },
	                error: function (jqxhr, status, errorThrown) {
	            		jQuery.ajax = oldAjax;
	            		$.ajax({
			                url: siteToanalyze,
			                type : 'GET',
			                success: function (result) {
								content = result
								analyzeCode(content, siteToanalyze, pages, 'Page')
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
    });
});

function analyzeCode(content, url, pages, reqType){
	var allVals = [];
	var prio = 1; 	
	var disabVal = 30;
    
	var prio = $('#priority').val();
    $('#disability :checked').each(function () {
        allVals.push($(this).val());
    });
    var total = 1;
    for (var v in allVals){
    	total = total * parseInt(allVals[v])
    }
    disabVal = total;
    pages.user = $('#userid').val()
    //pages.siteName = $('#projName').val()
    console.log(pages.user)
    //The given root page is the first elem in pages collection
	pages.urls.push(url)
	pages.contents.push(content)
	pages.disabilities = allVals
	pages.priority = prio
	
	//post page collection in JSON
	if (reqType ==  null){
    	crawl(content); 
    	reqType = 'Site'
    	postJson('/pageCollection', pages);
    }
    
	
    postToUrl('/submitPage', {'content' : content,
    						  'url' : url,
    						  'disabilities' : disabVal,
    						  'reqType' : reqType,
    						  'siteName' : pages.siteName,
    						  'priority' : prio}, asJson = false);
}


//Need a test for localhost connection
function isValidURL(url){
    var RegExp = /(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/;
    return RegExp.test(url);
} 

//stores the descendant urls of the submitted url
function crawl(content){
	
	$(content).find('a').each(function(idx, item){
		var url = $(this).attr('href');
		//Need a more accurate check for localhost urls
		if (pages.urls.indexOf(url) == -1){
			if(!isValidURL(url)){
				
				$.ajax({
		                url: url,
		                type : 'GET',
		                async : false,
		                dataType : "html",
		                success: function (result) {
		                    content = result;
		                    pages.urls.push(url)
		                    pages.contents.push(content)
		                    crawl(content)
		                },
		                error: function (jqxhr, status, errorThrown) {
		                    alert(jqxhr.responseText);
		                }
		            });
	        }
       }
	})
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


