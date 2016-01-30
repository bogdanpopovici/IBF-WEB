
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

