
$(function(){   
    $("#lofinform").on('submit', function(e){
        var isvalidate=$("#lofinform").valid();
        if(isvalidate)
        {
            e.preventDefault();
            alert(getvalues("lofinform"));
        }
    });
});

function getvalues(f)
{
    var form=$("#"+f);
    var str='';
    $("input:not('input:submit')", form).each(function(i){
        str+='\n'+$(this).prop('name')+': '+$(this).val();
    });
    return str;
}

$(".a").on("click", function(event){
    if ($(this).is("[disabled]")) {
        event.preventDefault();
    }
});



function popUpNotificationModal(item_id, pwoc, contact_details){

  if (pwoc=='IBF'){
    $('#notification_text').text("Hi! The finder would like to use our dedicated messaging service. Go On ! Leave him/her a message to get in contact...");
    $('#notification_creator').click(function(){
      $.post('/API/notify/',{
          'method': 'IBF',
          'message':   $('#notification_message').val(),
          'item_id':   item_id,
          'csrfmiddlewaretoken':      $('[name="csrfmiddlewaretoken"]').val()
      },function(result){
          if(result.result=='OK'){
              location.reload();
          }
          else{
            alert("An error occured. Please get in contact with the support team");
          }
      });
    });
        
  }
  else 
  if (pwoc=='EMAIL'){
    $('#notification_text').text("Hi! The finder would like to use his/her email address to get in contact.  Go on! Add your message and will take care of the rest...");
    $('#notification_creator').click(function(){
      $.post('/API/notify/',{
          'method': 'email',
          'message':   $('#notification_message').val(),
          'item_id':   item_id,
          'csrfmiddlewaretoken':      $('[name="csrfmiddlewaretoken"]').val()
      },function(result){
          if(result.result=='OK'){
              location.reload();
          }
          else{
            alert("An error occured. Please get in contact with the support team");
          }
      });
    });


  } else {
    $('#notification_text').text("Hi! The finder would like to contact him by phone, here's his/her number: " + contact_details + ", so please get in touch before claiming the item.");
    $('#notification_message').css('display','none')
    $('#notification_creator').click(function(){
      $.post('/API/notify/',{
          'method': 'phone',
          'item_id':   item_id,
          'csrfmiddlewaretoken':      $('[name="csrfmiddlewaretoken"]').val()
      },function(result){
          if(result.result=='OK'){
              location.reload();
          }
          else{
            alert("An error occured. Please get in contact with the support team");
          }
      });
    });
  }

  $('#notificationModal').modal('toggle');

}

function popUpItemModal(description, category, finder, location, date, time){

  $('#decription').text(description);
  $('#decrcategoryiption').text(category);
  $('#finder').text(finder);
  $('#location').text(location);
  $('#dateNTime').text(date + time);

  $('#itemModal').modal('toggle');

}

$(document).ready( function() {
    get_notifications();
setInterval(function() {
    get_notifications();
}, 30000);
});

function get_notifications(){

  if($("#notifications-no")){
    $.get('/API/get_notifications/',{
    },function(result){
        if(result.result=='OK'){

            var notifications = result.notifications;
            var messages = result.messages;
            $("#notifications-no").html(notifications.length);
            $("#messages-no").html(messages.length);
            $("#notifications-top-container").empty();
            $("#messages-top-container").empty();

            if(notifications.length !=0){
               notifications.forEach(function (item){
                  $("#notifications-top-container").append('<div><h4 class="item-title">Match found for item:</h4>'+
                    '<a href="/myaccount/5/" class="item-info">'+ item.item +'</a></div>');
               });

            } else {
              $("#notifications-top-container").append('<div><h4 class="empty-title">There are no new matches found for any of your lost items.</h4>'+
                 '<p class="empty-tip">To see old conversations go to the "Notifications" Tab inside </p>'+
                 '<a href="/myaccount/5/">MyAccount</a></div>');

            }

            if(messages.length !=0){
              messages.forEach(function (item){
                  $("#messages-top-container").append('<div><h4 class="item-title">Message: '+messsage.message+'</h4>'+
                   '<a href="/myaccount/4/" class="item-info">From: '+message.sender+'</a></div>');
               });

            } else {
              $("#messages-top-container").append('<div><h4 class="empty-title">There are no new matches found for any of your lost items.</h4>'+
                 '<p class="empty-tip">To see old conversations go to the "Notifications" Tab inside </p>'+
                 '<a href="/myaccount/4/">MyAccount</a></div>');

            }
        }
        else{
        }
    });
  }
  
}

function seeItem() {
  
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