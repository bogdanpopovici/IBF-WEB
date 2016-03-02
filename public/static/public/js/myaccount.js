var new_item_title = ''
var new_item_description = ''
var new_item_category  = ''
var new_item_uid =''
var new_item_files = []

function previewItem(media_uri) {
	
  new_item_title = $('#titleid').val();
  new_item_category = $('#categoryid').val();
  new_item_description = $('#descriptionid').val();
  new_item_uid = $('#uid').val();

  $('#preview-modal').modal('toggle');

  var p_title = $('#preview_title');
  var photosContainer = $('#preview-photos-container');
  var p_desc = $('#preview_desc');
  var p_uid = $('#preview_uid');

  p_title.html(new_item_title);
  p_desc.html(new_item_description);
  photosContainer.empty();

  if (new_item_uid != ''){
  	p_uid.html(new_item_uid);
  	p_uid.removeClass("hideIt");
  }
  else{
  	p_uid.addClass("hideIt");
  }
  
  $("img.file-preview-image").each(function( index ) {
    new_item_files.push(JSON.stringify(getBase64Image(this)));

    var photo = this;
    var div = $("<div></div>");

    div.addClass("item");
    div.addClass("carousel-photo");

    if(index==0)
	    div.addClass("active");

    div.append(this);
    photosContainer.append(div);
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
function updateItem(title, uid, description, category,  media, media_uri){
	$('#u_titleid').val(title);
	$('#u_descriptionid').val(description);
	$('#u_uid').val(uid);
	$('#u_categoryid').val(category);
	$('#update-modal').modal('toggle');

	var photos = JSON.parse(media);
	console.log(photos);

	 for(var i=0;i<photos.length;i++) {
	    var photo = media_uri+photos[i].fields.data;

	    $('.file-preview-thumbnails').append('<div class="file-preview-frame" id="preview-1455980621246-0" data-fileindex="0">'+
										          '<img src="'+photo+'" class="file-preview-image" style="width:auto;height:80px;">'+
											      '<div class="file-thumbnail-footer">'+
											          '<div class="file-footer-caption" title="global_del.png">global_del.png</div>'+
											          '<div class="file-thumb-progress hide">'+
											          	'<div class="progress">'+
											          		'<div class="progress-bar progress-bar-success progress-bar-striped active" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width:0%;">0%+</div>'+
											          	'</div>'+
											          '</div>'+
												      '<div class="file-actions">'+
											              '<div class="file-footer-buttons"><button type="button" class="kv-file-remove btn btn-xs btn-default" title="Remove file"><i class="glyphicon glyphicon-trash text-danger"></i></button></div>'+
											              '<div class="file-upload-indicator" title="Not uploaded yet"><i class="glyphicon glyphicon-hand-down text-warning"></i></div>'+
											              '<div class="clearfix"></div>'+
												       '</div>'+
													'</div>'+
											 '</div>');
		}

	$('#update-modal').modal('toggle');
	

	//$('u_titleid').val(title);
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
					document.getElementById('s6').innerHTML = result.new_value
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

  $('#preRegisterButton').prop('disabled', true);
  $('#preRegisterButton').html('<span class="glyphicon glyphicon-refresh spinning"></span> Registering...');
  $.post('/API/item_pre_registration/',{
        'uniqueid':   new_item_uid,
        'category':   new_item_category,
        'description':   new_item_description,
        'tags':   new_item_title,
        'media1':   new_item_files[0],
        'csrfmiddlewaretoken':      $('[name="csrfmiddlewaretoken"]').val()
    },function(result){
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

function deleteItem(pk){
  $.post('/API/delete_item/',{
        'pk':   pk,
        'csrfmiddlewaretoken':      $('[name="csrfmiddlewaretoken"]').val()
    },function(result){
        if(result.result=='OK'){
          window.location = "/myaccount/4/";
        }
        else{
          alert("An error has occured while uploading yur file");
        }
    });
}