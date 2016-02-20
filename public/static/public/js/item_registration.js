var ui;
var title;
var category;
var description;
var tags;
var location_text;
var files;
var cont;

$("#file-upload-input").fileinput({
    uploadUrl: '#', // you must set a valid URL here else you will get an error
    allowedFileExtensions : ['jpg', 'png','gif'],
    overwriteInitial: false,
    maxFileSize: 1000,
    maxFilesNum: 10,
    //allowedFileTypes: ['image', 'video', 'flash'],
    slugCallback: function(filename) {
        return filename.replace('(', '_').replace(']', '_');
    }
});
$("#pac-input").bind("keydown", function(e) { if (e.keyCode === 13) return false; });
$("#upload-item-form").on('keyup keypress', function(e) {
  var keyCode = e.keyCode || e.which;
  if (keyCode === 13) { 
    e.preventDefault();
    return false;
  }
});

function previewItem(is_authenticated, user){
  ui = $('#uid').val();
  title = $('#titleid').val();
  category = $('#categoryid').val();
  description = $('#descriptionid').val();
  tags = $('#tagsid').val();
  location_text = $('#pac-input').val();
  files = [];
  cont = true;
  
  var myDate = new Date();
  var displayDate = (myDate.getMonth()+1) + '/' + (myDate.getDate()) + '/' + myDate.getFullYear();
  var photosContainer = $('#photos-container');
  photosContainer.empty();

  if(ui!=""){
    $('#prev_uid').html(ui);
  }else {
    $('#prev_uid').addClass('hideIt');
  }
  $('#prev_title').html(title);
  $('#prev_category').html(category);
  $('#prev_description').html(description);
  $('#prev_tags').html(tags);
  $('#prev_location').html(location_text);
  $('#prev_dateNTime').html(displayDate);
  $('#prev_finder').html(user);


  $('#upload-item-form').bootstrapValidator('validate');

  if(is_authenticated!="True"){
      $('#loginRequiredModal').modal('toggle');
      cont = false;
  }
  if(tags==""){
    $('#emptytagserror').removeClass('hide');
    cont = false;
  } else {
    $('#emptytagserror').addClass('hide');
  }
  
  $("img.file-preview-image").each(function( index ) {
    
    files.push(JSON.stringify(getBase64Image(this)));

    var photo = this;
    var div = $("<div></div>");

    div.addClass("item");
    div.addClass("carousel-photo");

    if(index==0)
      div.addClass("active");
    div.append(this);
     photosContainer.append(div);
  });


  if(cont && form_is_valid()){
      $('#previewModal').modal('toggle');
  }
}

function uploadData(){

  $('#submitButton').html('<span class="glyphicon glyphicon-refresh spinning"></span> Loading...');

  $('#submitButton').prop('disabled', true);
  $('#cancelSubmissionButton').prop('disabled', true)

  $.post('/item_registration/',{
        'uniqueid':   ui,
        'title': title,
        'category':   category,
        'description':   description,
        'tags':   tags,
        'location': location_text,
        'media':   JSON.stringify(files),
        'csrfmiddlewaretoken':      $('[name="csrfmiddlewaretoken"]').val()
    },function(result){
        if(result.result=='OK'){
           window.location = "/item_registration_confirmation/"+result.pk+"/";
           console.log("yes");
        }
        else{
          alert("An error has occured while uploading yur file");
        }
    });
}

function getBase64Image(imgElem) {
    var canvas = document.createElement("canvas");
    canvas.width = imgElem.naturalWidth;
    canvas.height = imgElem.naturalHeight;
    var ctx = canvas.getContext("2d");
    ctx.drawImage(imgElem, 0, 0);
    var dataURL = canvas.toDataURL("image/png");
    return dataURL.replace(/^data:image\/(png|jpg);base64,/, "");
}

function form_is_valid(){
    var result = true;
    $('.form-group').each(function(){
        if($(this).hasClass('has-error')){
            result = false;
            return false;
        }
    });
    return result;
}

function initMap() {
  var map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 51.531298, lng: -0.120851},
    zoom: 7
  });
  var input = /** @type {!HTMLInputElement} */(
      document.getElementById('pac-input'));

  var types = document.getElementById('type-selector');
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(types);

  var autocomplete = new google.maps.places.Autocomplete(input);
  autocomplete.bindTo('bounds', map);

  var infowindow = new google.maps.InfoWindow();
  var marker = new google.maps.Marker({
    map: map,
    anchorPoint: new google.maps.Point(0, -29)
  });

  autocomplete.addListener('place_changed', function() {
    infowindow.close();
    marker.setVisible(false);
    var place = autocomplete.getPlace();
    if (!place.geometry) {
      window.alert("Autocomplete's returned place contains no geometry");
      return;
    }

    if (place.geometry.viewport) {
      map.fitBounds(place.geometry.viewport);
    } else {
      map.setCenter(place.geometry.location);
      map.setZoom(17);  
    }
    marker.setIcon( ({
      url: place.icon,
      size: new google.maps.Size(71, 71),
      origin: new google.maps.Point(0, 0),
      anchor: new google.maps.Point(17, 34),
      scaledSize: new google.maps.Size(35, 35)
    }));
    marker.setPosition(place.geometry.location);
    marker.setVisible(true);

    var address = '';
    if (place.address_components) {
      address = [
        (place.address_components[0] && place.address_components[0].short_name || ''),
        (place.address_components[1] && place.address_components[1].short_name || ''),
        (place.address_components[2] && place.address_components[2].short_name || '')
      ].join(' ');
    }

    infowindow.setContent('<div><strong>' + place.name + '</strong><br>' + address);
    infowindow.open(map, marker);
  });

}
