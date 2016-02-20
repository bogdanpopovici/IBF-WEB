
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



function popUpNotificationModal(item_id, pwoc, user_registered, contact_details){

  if(user_registered!="True"){
      $('#loginRequiredModal').modal('toggle');
  }
  else{

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

  

}

function popUpItemModal(uid, title, description, tags, category, finder, location, date, time, media, media_uri){

  
  var photosContainer = $('#details-photos-container');
  photosContainer.empty();

  if(uid!=""){
    $('#details_uid').html(uid);
  }else {
    $('#details_uid').addClass('hideIt');
  }
  $('#details_title').html(title);
  $('#details_category').html(category);
  $('#details_description').html(description);
  $('#details_tags').html(tags);
  $('#details_location').html(location);
  $('#details_dateNTime').html(date+" "+time);
  $('#details_finder').html(finder);
  

  var photos = JSON.parse(media);

  for(var i=0;i<photos.length;i++) {
    var photo = '<img src="'+media_uri+photos[i].fields.data+'" alt="...">';
    if(i==0)
      photosContainer.append('<div class="item carousel-photo active">'+photo+'</div>');
    else
      photosContainer.append('<div class="item carousel-photo">'+photo+'</div>');
  }


  $('#detailsModal').modal('toggle');
  
}

function add_image_to_carousel(element, index, array) {
    
  if(index==0){
    $('#carousel-indicators').append('<li data-target="#preview-carousel" data-slide-to="0" class="active"></li>');
    $('#carousel-inner').append('<div class="item active"><img src="'+ element +'" alt="photo of '+ description +'"></div>');
  } else{
    $('#carousel-indicators').append('<li data-target="#preview-carousel" data-slide-to="'+ index +'"></li>');
    $('#carousel-inner').append('<div class="item"><img src="'+ element +'" alt="photo of '+ description +'"></div>');
  }
  console.log('a[' + index + '] = ' + element);
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
            console.log(messages);
            $("#notifications-no").html(notifications.length);
            $("#messages-no").html(messages.length);
            $("#notifications-top-container").empty();
            $("#messages-top-container").empty();

            if(notifications.length !=0){
               notifications.forEach(function (item){
                  $("#notifications-top-container").append('<div><h4 class="item-title">Match found for item:</h4>'+
                    '<a href="/myaccount/6/" class="item-info">'+ item.item +'</a></div>');
               });

            } else {
              $("#notifications-top-container").append('<div><h4 class="empty-title">There are no new matches found for any of your lost items.</h4>'+
                 '<p class="empty-tip">To see old conversations go to the "Notifications" Tab inside </p>'+
                 '<a href="/myaccount/6/">MyAccount</a></div>');

            }

            if(messages.length !=0){
              messages.forEach(function (item){
                  $("#messages-top-container").append('<div><h4 class="item-title">Message: '+item.message+'</h4>'+
                   '<a href="/myaccount/5/" class="item-info">From: '+item.sender+'</a></div>');
               });

            } else {
              $("#messages-top-container").append('<div><h4 class="empty-title">There are no new matches found for any of your lost items.</h4>'+
                 '<p class="empty-tip">To see old conversations go to the "Notifications" Tab inside </p>'+
                 '<a href="/myaccount/5/">MyAccount</a></div>');

            }
        }
        else{
        }
    });
  }
  
}
