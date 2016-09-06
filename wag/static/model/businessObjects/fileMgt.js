	
	var file, xhr = false;
	
	//** fileMgt - Read data of accessibility features from XML file(KB)
	$(function() {
		var xmlFile = $("input#xmlFile").val();
		$.ajax({
			type: "GET",
			url: xmlFile,
			async : false,
			dataType: "xml",
			success: function (xml) {
				makeFeatureCollection(xml); 
			},
			error: function(response) { 
				console.error("knowledgeBase is missing");
				document.getElementById("feature").innerHTML = "Sorry, but I couldn't create an XMLHttpRequest"; 
			}
		});
	})

		
	function openWin() {
		if (file != undefined) {
			var fileName = file;
			console.log(file);
				// Chrome and Opera
				if ((new RegExp('fakepath')).test(fileName)) {
					var fileName = fileName.substr(12);
				}
				// IE
				else if ((new RegExp(':')).test(fileName)) {
					var sp = fileName.split('\\');
					var fileName = sp[sp.length-1];
				}
				
			var srcWin = window.open('../Tests/sample/'+fileName);
		}	
		else {
			alert("Please select a source file first !");
		}
	}
	
	function deploy() {
		var cd = ((($('#code').html()).replace(/\&lt;/g,"<")).replace(/\&gt;/g,">")).replace(/\<br>/g,'\n');
	
		newWin = window.open('','','width=700,height=500,left=300');
		newWin.document.write(cd);
	}
