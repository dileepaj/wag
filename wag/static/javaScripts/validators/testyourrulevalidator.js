$(document).ready(function() {
	var urlregex = new RegExp("^(http:\/\/www.|https:\/\/www.|ftp:\/\/www.|www.){1}([0-9A-Za-z]+\.)");
  	$("#btn_testRule").click(function(event) {
  		var url = $("#testpageUrl").val().trim();
  		var file_name = $("#upload_json").val().trim();
  		if(urlregex.test(url)) {
  			valid_url = true;			
  		} else {
  			valid_url = false;
  		}

  		if(file_name.length != 0 && valid_url) {
  			$("#frm_community_test").submit();
  		} else {
  			event.preventDefault();
  		}
  	});
 });