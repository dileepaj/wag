$(document).ready(function() {

    $("#id_txt_community_user_email").prop("disabled", false);
    $("#btn_upload_id" ).click(function() { 
        
        $.ajax({
            type : "POST",
            url : "/communityuploadajax",
            cache: false,
            async: false,
            enctype: 'multipart/form-data',
            data : 'json_val=' + $('#json_val_hidden').val().trim() + 
                    '&user_name=' + $('#id_txt_community_user_name').val().trim() + 
                    '&user_email=' + $('#id_txt_community_user_email').val().trim() + 
                    '&user_work=' + $('#id_txt_work_description').val().trim() +
                    '&task_info=' + $('#id_txt_task_description').val().trim(),

            success : function (data) {
		         $('#id_txt_community_user_name').val("");
                 $('#id_txt_community_user_email').val("");
                 $('#id_txt_work_description').val("");
                 $('#id_txt_task_description').val("");
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                    
            }
        });
	 });
});



