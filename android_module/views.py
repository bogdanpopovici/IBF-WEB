from django.shortcuts import render
from core.models import CustomUser
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
from core.models import *
import hashlib, datetime, random, json, re, traceback, base64
from django.core.management import call_command

@csrf_exempt
def upload_item(request):
  response_data = {}

  if request.method=='POST':
    try:
     body_unicode = request.body.decode('utf-8')
     body = json.loads(body_unicode)
     category = body['category']
     tags = body['tags']
     valuable = body['valuable']
     media =  body['media']

     new_item = Item()
     new_item.tags = tags
     new_item.description = valuable
     new_item.category = category
     new_item.date_field = datetime.datetime.now().strftime("%Y-%m-%d")
     new_item.time_field = datetime.datetime.now().strftime("%H:%M:%S") 
     new_item.found_by_user = CustomUser.objects.all()[:1].get()
     new_item.save()

     photo = Media()
     photo.of_item = new_item
     photo.media_type = "PHOTO" 
     save_base64image_to_media(photo, media)
     photo.save()

     call_command('update_index')

     response_data['result'] = 'OK'
    except Exception as e:
     response_data['result'] = 'ERROR'
     print traceback.print_exc()
 
  return HttpResponse(json.dumps(response_data), content_type="application/json")


def save_base64image_to_media(media_obj, data):
  img_temp = NamedTemporaryFile()
  img_temp.write(base64.b64decode(data))
  img_temp.flush()
  media_obj.data.save("media.jpg", File(img_temp))