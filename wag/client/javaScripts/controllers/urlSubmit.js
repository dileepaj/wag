//** View Controller

////////////////////////////////////////////URL submission/////////////////////////////////////////////////////////////

$(function () {

    $("#URLSubmit").click(function () {
    	alert("URL submitted");
    	
    	var siteToanalyze = $("#externURL").val();
        if (isValidURL(siteToanalyze)) {
            $.ajax({
                url: "http://127.0.0.1:5000/ALSI",
                success: function (result) {
                    alert(result);

                    //disability values
                    var allVals = [];
                    $('#disability :checked').each(function () {
                        allVals.push($(this).val());
                    });

                    //For evalData Can send one value with 3 bits
                    //Or send 3 bools
                    var postResult = {
                        content: result,
                        evalData: [{
                            priority: $('#priority').val(),
                            lowVision: allVals
                        }]
                    }
                    //var jqxhr =  $.post(
                   setSrcode(postResult.content);
                },
                error: function (jqxhr, status, errorThrown) {
                    alert(status);
                }
            });
        } else {
            alert("enter valid URL");
        }
    });
});

function isValidURL(url){
    var RegExp = /(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/;

    return RegExp.test(url);
} 