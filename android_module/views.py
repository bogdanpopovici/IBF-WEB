from django.shortcuts import render
from core.models import CustomUser
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
from core.models import *
import hashlib, datetime, random, json, re, traceback, base64, string
from django.core.management import call_command
from django.contrib.auth import authenticate

@csrf_exempt
def upload_item(request):
  response_data = {}

  if request.method=='POST':
    try:
     body_unicode = request.body.decode('utf-8')
     body = json.loads(body_unicode)

     try:
      username = body['username']
      finder =  CustomUser.objects.filter(username=username)
     except:
      finder = None

     if not finder:
      password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
      email = body['email']

      finder = CustomUser()
      finder.username = username
      finder.email = email
      finder.prefered_way_of_contact = "IBF"
      finder.set_password(password)
      dinder.save()
      

      salt = hashlib.sha1(str(random.random())).hexdigest()[:5]            
      activation_key = hashlib.sha1(salt+email).hexdigest()            
      key_expires = datetime.datetime.today() + datetime.timedelta(2)

      # Create and save user profile                                                                                                                                  
      new_profile = UserProfile(user=finder, activation_key=activation_key, 
          key_expires=key_expires)
      new_profile.save()

      # Send email with activation key
      email_subject = 'Account confirmation'
      email_body = "Hey %s, thanks for uploading the item. We have created an account for you.\n To activate your account, click this link within \
      48hours http://127.0.0.1:8000/accounts/confirm/%s. \n Your username: %s \n Your password: %s \n" % (username, activation_key, username, password)

      send_mail(email_subject, email_body, 'myemail@example.com',
          [email], fail_silently=False)

     category = body['category']
     tags = body['tags']
     location = body['location']
     valuable = body['valuable']
     media =  body['media']

     new_item = Item()
     new_item.tags = tags
     new_item.description = valuable
     new_item.category = category
     new_item.location = location
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


@csrf_exempt
def login_user(request):
  response_data = {}

  if request.method=='POST':
    try:
     body_unicode = request.body.decode('utf-8')
     body = json.loads(body_unicode)
     username = body['username']
     password = body['password']

     user = authenticate(username=username, password=password)
     if user is not None:
       response_data['result'] = 'OK'
       response_data['username'] = user.username
       response_data['first_name'] = user.first_name
       response_data['last_name'] = user.last_name
     else:
       response_data['result'] = 'ERROR'
       response_data['message'] = 'Username or password do not match !!'
       
    except Exception as e:
     response_data['result'] = 'ERROR'
     print traceback.print_exc()
 
  return HttpResponse(json.dumps(response_data), content_type="application/json")

def save_base64image_to_media(media_obj, data):
  img_temp = NamedTemporaryFile()
  img_temp.write(base64.b64decode(data))
  img_temp.flush()
  media_obj.data.save("media.jpg", File(img_temp))