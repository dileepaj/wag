//*** the script runs when target source file is opened and 
//*** parse the XMLSerialized string of it's document 

window.onload = function() { 
	if ( window.opener != null ) {  
		var serializer = new XMLSerializer ();
		var str = serializer.serializeToString (document);
		window.opener.setSrcode(str); 
		window.close();
	}
 }