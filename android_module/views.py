from django.shortcuts import render
from core.models import CustomUser
import hashlib, datetime, random, json, re, traceback, base64

def upload_item(request):
  response_data = {}

  if request.method=='POST':
    try:
     category = request.POST.get('category')
     tags = request.POST.get('tags')
     valuable = request.POST.get('valuable')

     new_item = Item()
     new_item.tags = tags
     new_item.tags = valuable
     new_item.category = category
     new_item.date_field = datetime.datetime.now().strftime("%Y-%m-%d")
     new_item.time_field = datetime.datetime.now().strftime("%H:%M:%S") 
     new_item.found_by_user = CustomUser.objects().filter(pk=1)
     new_item.save()

     call_command('update_index')
     response_data['result'] = 'OK'
    except Exception as e:
     response_data['result'] = 'ERROR'
     response_data['message'] = traceback.print_exc()
 
  return HttpResponse(json.dumps(response_data), content_type="application/json")