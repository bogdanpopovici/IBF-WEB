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
function uploadData(user){

  var ui = $('#uid').val();
  var category = $('#categoryid').val();
  var description = $('#descriptionid').val();
  var tags = $('#tagsid').val();
  var location = $('#pac-input').val();
  var files = [];
  var cont = true;

  $('#upload-item-form').bootstrapValidator('validate');

  if(user!="True"){
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
  });

  if(cont && form_is_valid()){

    $('#submitButton').html('<span class="glyphicon glyphicon-refresh spinning"></span> Loading...');

    //$('#submitButton').prop('disabled', true);

    $.post('/item_registration/',{
          'uniqueid':   ui,
          'category':   category,
          'description':   description,
          'tags':   tags,
          'location': location,
          'media':   JSON.stringify(files),
          'csrfmiddlewaretoken':      $('[name="csrfmiddlewaretoken"]').val()
      },function(result){
          if(result.result=='OK'){
             window.location.reload();
          }
          else{
            alert("An error has occured while uploading yur file");
          }
      });
  }
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
    center: {lat: -33.8688, lng: 151.2195},
    zoom: 13
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

    // If the place has a geometry, then present it on a map.
    if (place.geometry.viewport) {
      map.fitBounds(place.geometry.viewport);
    } else {
      map.setCenter(place.geometry.location);
      map.setZoom(17);  // Why 17? Because it looks good.
    }
    marker.setIcon(/** @type {google.maps.Icon} */({
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

  // Sets a listener on a radio button to change the filter type on Places
  // Autocomplete
}
