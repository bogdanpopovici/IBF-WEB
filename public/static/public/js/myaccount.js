var new_item_title = ''
var new_item_description = ''
var new_item_category  = ''
var new_item_uid =''
var new_item_files = []

function previewItem() {
	
  new_item_title = $('#titleid').val();
  new_item_category = $('#categoryid').val();
  new_item_description = $('#descriptionid').val();
  new_item_uid = $('#uid').val();
  
  $("img.file-preview-image").each(function( index ) {
     new_item_files.push(JSON.stringify(getBase64Image(this)));
  });

  $('#preview-modal').modal('toggle');

  var p_title = $('#preview_title');
  var p_photos = $('#preview_photos');
  var p_desc = $('#preview_desc');
  var p_uid = $('#preview_uid');

  p_title.html(new_item_title);
  p_desc.html(new_item_description);

  if (new_item_uid != ''){
  	p_uid.html(new_item_uid);
  	p_uid.removeClass("hideIt");
  }
  else{
  	p_uid.addClass("hideIt");
  }
  
  $("img.file-preview-image").each(function( index ) {
     p_photos.append(this);
  });
}

function backToEdit(){
  $('#preview-modal').modal('toggle');
}

function getBase64Image(imgElem) {
// imgElem must be on the same server otherwise a cross-origin error will be thrown "SECURITY_ERR: DOM Exception 18"
    var canvas = document.createElement("canvas");
    canvas.width = imgElem.naturalWidth;
    canvas.height = imgElem.naturalHeight;
    var ctx = canvas.getContext("2d");
    ctx.drawImage(imgElem, 0, 0);
    var dataURL = canvas.toDataURL("image/png");
    return dataURL.replace(/^data:image\/(png|jpg);base64,/, "");
} 


function toggle(input, value, option, field) {
	var it = document.getElementById(input);
	var v = document.getElementById(value);
	var o = document.getElementById(option);

	if(it.style.display == "block") {

		$.post('/edit_personal_details/',{
		    'field':   field,
		    'value':   it.value,
		    'csrfmiddlewaretoken':      $('[name="csrfmiddlewaretoken"]').val()
		},function(result){
		    if(result.result=='OK'){
		        v.innerHTML = result.new_value;
		        it.value = ''
		    }
		    else{
		    	alert(result.err_message);
		    }
		});

    	it.style.display = "none";
		o.innerHTML = "Edit";
		v.style.display = "block";
  	}
	else {
		reset();
		it.style.display = "block";
		o.innerHTML = "Save";
		v.style.display = "none";
	}
}

function change_settings(container, input1, input2, input3, value, option, field) {
	var c = document.getElementById(container);
	var it1 = document.getElementById(input1);
	var it2 = document.getElementById(input2);
	var it3 = document.getElementById(input3);
	var v = document.getElementById(value);
	var o = document.getElementById(option);

	if(c.style.display == "block") {

		$.post('/edit_personal_details/',{
		    'field':    field,
		    'value1':   it1.value,
		    'value2':   it2.value,
		    'value3':   it3.value,
		    'csrfmiddlewaretoken':      $('[name="csrfmiddlewaretoken"]').val()
		},function(result){
		    if(result.result=='OK'){
		        it1.value = '';
		        it2.value = '';
		        it3.value = '';

		        if(field == "email")
					document.getElementById('s7').innerHTML = result.new_value
		    }
		    else{
		    	alert(result.err_message);
		    }
		});

    	c.style.display = "none";
		o.innerHTML = "Edit";
		v.style.display = "block";

  	}
	else {
		reset();
		c.style.display = "block";
		o.innerHTML = "Save";
		v.style.display = "none";
	}
}

function reset() {
	for (i = 1; i <= 6; i++) {

			var it = document.getElementById('it'+i);
    		it.style.display = "none";
			var v =document.getElementById('s'+i);
    		v.style.display = "block";
			var o = document.getElementById('e'+i);
			o.innerHTML = "Edit";
  		}

  		var itp1 = document.getElementById('itp1');
		it1.innerHTML = "";
		var itp2 = document.getElementById('itp2');
		it2.innerHTML = "";
		var itp3 = document.getElementById('itp3');
		it3.innerHTML = "";
}

function reply_to_notification(seq_index, topic_pk){
	var it = $("#message_input_"+seq_index);
	var container = $("#message_box_"+seq_index);
	var message = it.val();

	$.post('/API/reply_to_notification/',{
		    'notification_pk':   topic_pk,
		    'message': message,
		    'csrfmiddlewaretoken':      $('[name="csrfmiddlewaretoken"]').val()
		},function(result){
		    if(result.result=='OK'){
		    	var new_message = jQuery('<div class="row no-margin"> <div class="message-sent">'+ message +'</div> </div>').hide();
		        container.append(new_message)
		        new_message.show('slow');
		        it.val('');
		    }
		    else{
		    	alert(result.err_message);
		    }
		});
}

function pre_register_item(media_url){

	console.log("in");
  $.post('/API/item_pre_registration/',{
        'uniqueid':   new_item_uid,
        'category':   new_item_category,
        'description':   new_item_description,
        'tags':   new_item_title,
        'media1':   new_item_files[0],
        'csrfmiddlewaretoken':      $('[name="csrfmiddlewaretoken"]').val()
    },function(result){
    	console.log("out");
        if(result.result=='OK'){


          $('#preview-modal').modal('toggle');
          $('#pre-register-modal').modal('toggle');
          $('.registered-items').append(
              '<li class="row registered-item">'+
                '<div class="col-md-3"><img src="'+result.image+'" class="img-responsive center-block"></img></div>'+
                '<div class="col-md-6 text-muted"><label class="panel-title" id="s6">'+new_item_title+'</label><hr><p>'+new_item_category+
                '</p></div><div class="col-md-3 text-right"><label><a id="e6" href="">Update</a></label></div></li>'
            );

        }
        else{
          alert("An error has occured while uploading your file");
        }
    });
}


function repatriate_item(item_id){
	console.log("okk");
	$.post('/API/repatriate_item/',{
        'item_id':   item_id,
        'csrfmiddlewaretoken':      $('[name="csrfmiddlewaretoken"]').val()
    },function(result){
        if(result.result=='OK'){
           $('#repatriate_button_found_'+item_id).html('Waiting...');
           $('#repatriate_button_found_'+item_id).addClass('active');
        }
        else{
          alert("An error has occured while uploading yur file");
        }
    });
}


function rejectNotification(notification_id){

    bootbox.confirm("Are you sure this is not yours? You won't be notified on this item in the future!", function(result) {
      
      if(result){
	      $.post('/API/reject_match/',{
	      'notification_id':   notification_id,
	      'csrfmiddlewaretoken':      $('[name="csrfmiddlewaretoken"]').val()
	      },function(result){
	          if(result.result=='OK'){
	              $('#match_'+notification_id).remove();
	          }
	          else{
	            alert("An error occured. Please get in contact with the support team");
	          }
	      });
		}
	 }); 
}


function open_tab(tab){

	var i;
	for(i=1;i<=6;i++){
		$('#ltab'+i).removeClass('active');
		$('#tab'+i).removeClass('active');
	}

	$('#ltab'+tab).addClass('active');
	$('#tab'+tab).addClass('active');

}


function respond_to_repatriation(response, notification_id, seq_index){

	var container = $("#message_box_"+seq_index);

	$.post('/API/respond_to_repatriation/',{
	      'notification_id':   notification_id,
	      'response':   response,
	      'csrfmiddlewaretoken':      $('[name="csrfmiddlewaretoken"]').val()
	      },function(result){
	          if(result.result=='OK'){
				   	$('#yes_button_'+notification_id).remove();
				   	$('#no_button_'+notification_id).remove();
				   	var new_message = jQuery('<div class="row no-margin"> <div class="message-sent">'+ result.message +'</div> </div>').hide();
			        container.append(new_message)
			        new_message.show('slow');
	          }
	          else{
	            alert("An error occured. Please get in contact with the support team");
	          }
	      });

	
}