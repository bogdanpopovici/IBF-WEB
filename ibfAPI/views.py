#  --- University of Southampton ---
#  --- Group Design Project in collaboration with 'The Big Consulting' ---
#  --- Copyright 2015 ---

import hashlib, datetime, random, json, re, traceback, base64, string
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, get_object_or_404
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils import timezone
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
from django.core.management import call_command
from django.contrib.auth import get_user_model
from social.backends.oauth import BaseOAuth1, BaseOAuth2
from social.backends.google import GooglePlusAuth
from social.backends.utils import load_backends
from social.apps.django_app.utils import psa
from core.forms import RegistrationForm
from core.models import UserProfile, Item, PreRegisteredItem, Media, Notification
from core.settings import MEDIA_URL
from collections import defaultdict
from public.decorators import render_to
from itertools import chain
from search_engine.views import ItemsMatchView
  
# ----------------------------------------------------------------------------------------
# Username check - Local function
# ----------------------------------------------------------------------------------------

def check_username_ok(un):
  # Check if the username matches a username already in the database
  try:
    user = get_user_model().objects.get(username=un)
    return False
  except get_user_model().DoesNotExist:
    return True

# ----------------------------------------------------------------------------------------
# Username check - Accessed by URL 
# ----------------------------------------------------------------------------------------

def username_check(request):
  response_data = {}
  
  response_data['valid'] = check_username_ok(request.GET.get("username"))
 
  return HttpResponse(json.dumps(response_data), content_type="application/json")


# ----------------------------------------------------------------------------------------
# Email check - Local Function
# ----------------------------------------------------------------------------------------

def email_check_ok(email_address):
  # Check if the username matches a username already in the database
  try:
    user = get_user_model().objects.get(email=email_address)
    return False
  except get_user_model().DoesNotExist:
    return True


# ----------------------------------------------------------------------------------------
# Email check - Accessed by URL 
# ----------------------------------------------------------------------------------------

def email_check(request):
  response_data = {}
  response_data['valid'] = email_check_ok(request.GET.get("email"))
  return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required
def reply_to_notification(request):

  if request.method=='POST':
    try:
      old_notification = Notification.objects.filter(pk=request.POST.get('notification_pk'))[0]
      sender = request.user
      if old_notification.sender == sender:
        receiver = old_notification.receiver
      else:
        receiver = old_notification.sender
      response_data = {}

      message = request.POST.get('message')
      notification = Notification()
      notification.sender = sender
      notification.receiver = receiver
      notification.notification_type = "CLAIM"
      notification.message = message
      notification.topic = old_notification.topic
      notification.save()
      response_data['result'] = 'OK'
    except Exception, e:
      traceback.print_exc()
      response_data['result'] = 'ERROR'
  
  return HttpResponse(json.dumps(response_data), content_type="application/json")
  
@login_required
def item_pre_registration(request):

  image = None

  if request.method=='POST':
    try:
     uid = request.POST.get('uniqueid')
     category = request.POST.get('category')
     description = request.POST.get('description')
     tags = request.POST.get('tags')
     media = request.POST.get('media1')

     new_item = PreRegisteredItem()
     new_item.unique_id = uid
     new_item.tags = tags
     new_item.description = description
     new_item.category = category 
     new_item.owner = request.user
     new_item.save()

     photo = Media()
     photo.of_item = new_item
     photo.media_type = "PHOTO" 
     save_base64image_to_media(photo, media)
     photo.save()
     image = photo.data
     
     return HttpResponse(json.dumps({'result': 'OK', 'image':image.url}), content_type="application/json")
    except Exception as e:
     traceback.print_exc()
     return HttpResponse(json.dumps({'result': 'ERROR'}), content_type="application/json")

@login_required
def notify(request):

  if request.method=='POST':
    try:
      item = Item.objects.filter(pk=request.POST.get('item_id'))[0]
      sender = request.user
      receiver = item.found_by_user
      response_data = {}

      method =  request.POST.get('method')
      message = request.POST.get('message')

      if (method == 'IBF'):
        notification = Notification()
        notification.sender = sender
        notification.receiver = receiver
        notification.message = message
        notification.topic = item
        notification.notification_type = 'CLAIM'
        notification.save()
        item.status = 'CLAIMED'
        item.lost_by_user = sender
        item.save()
        response_data['result'] = 'OK'

      elif (method == 'email'):
        email_subject = 'IBF: Claimed Item'
        email_body = "Hey %s, someone is claiming one of the items you found. Here's his email address so you can get in touchL %s" % (receiver.username, sender.email)

        send_mail(email_subject, email_body, 'myemail@example.com',
              [receiver.email], fail_silently=False)
        item.status = 'CLAIMED'
        item.lost_by_user = sender
        item.save()
        response_data['result'] = 'OK'

      elif (method == 'phone'):
        item.status = 'CLAIMED'
        item.lost_by_user = sender
        item.save()
        response_data['result'] = 'OK'
    except Exception, e:
      traceback.print_exc()
      response_data['result'] = 'ERROR'
  
  return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required
def repatriate_item(request):
  response_data = {}
  if request.method=='POST':
    try:
     item_id = request.POST.get('item_id')
     item = Item.objects.filter(pk=item_id)[0]
     item.status = "PREREPATRIATED"
     item.save()

     notification = Notification()
     notification.sender = item.found_by_user
     notification.receiver = item.lost_by_user
     notification.message = item.found_by_user.username + ' wants to mark this item (subject of this conversation) as "Repatriated". If you agreed with the finder on a metting, then please accept his request.'

     notification.topic = item
     notification.notification_type = 'ACCEPT'
     notification.save()
     response_data['result'] = 'OK'
    except Exception, e:
      traceback.print_exc()
      response_data['result'] = 'ERROR'
  
  return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required
def reject_match(request):

  response_data = {}

  if request.method=='POST':
    try:
      notification = Notification.objects.filter(pk=request.POST.get('notification_id'))[0]

      notification.notification_type = "REJECT"
      notification.save()
      response_data['result'] = 'OK'
    except Exception, e:
      traceback.print_exc()
      response_data['result'] = 'ERROR'

  return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required
def respond_to_repatriation(request):

  response_data = {}
  if request.method=='POST':
    try:
      notification = Notification.objects.filter(pk=request.POST.get('notification_id'))[0]

      response = request.POST.get('response')

      
      notification = Notification.objects.filter(pk=request.POST.get('notification_id'))[0]
      item = Item.objects.filter(pk=notification.topic.pk)[0]
      notification.notification_type = "CLAIM"

      new_notification = Notification()
      new_notification.sender = request.user
      new_notification.receiver = notification.sender
      if response == 'true':
        new_notification.message = "Congratulations!! "+notification.topic.tags + " has been repatriated."
        new_notification.notification_type = 'CLAIM'
        item.status = "REPATRIATED"
        item.save()
      else:
        new_notification.message = request.user.username + " and you have to agree how the repatriation will occur. Once this is done, you can request a 'Repatriated' status change on "+notification.topic.tags
        new_notification.notification_type = 'CLAIM'
        item.status = "CLAIMED"
        item.save()
      new_notification.topic = item
      new_notification.notification_type = 'CLAIM'
      new_notification.save()      
      response_data['message'] = new_notification.message
      notification.save()
      response_data['result'] = 'OK'
    except Exception, e:
      traceback.print_exc()
      response_data['result'] = 'ERROR'

  return HttpResponse(json.dumps(response_data), content_type="application/json")


def notifications_job(request):
  data = None
  log =''
  try:
    match_search = ItemsMatchView()
    pre_reg_items = PreRegisteredItem.objects.filter(lost=True)

    log += "<p>=========================</p>"
    log += "<p>======= START JOB =======</p>"

    for item in pre_reg_items:
      log+= "<p>== Searching matches for item:</p>"
      log+= "<p>______Title: "+item.tags+"</p>"
      log+= "<p>______Category: "+item.category+"</p>"
      log+= "<p>______Created on: "+str(item.created_at)+"</p>"
      t= request.GET.copy()
      t.update({'q': string.replace(item.tags,' ','+')})
      t.update({'category': item.category})
      t.update({'unique_id': item.unique_id})
      t.update({'start_date': str(item.created_at).split(' ')[0]})
      request.GET = t
      match_results = match_search.get(request)
      for match in match_results:
        if not Notification.objects.filter(notification_type="MATCH", match=item, topic=match.object):
          log+= "<p>== Creating notification for match:</p>"
          log+= "<p>______Title: "+match.object.tags+"</p>"
          log+= "<p>______Category: "+match.object.category+"</p>"
          log+= "<p>______Created on: "+str(match.object.date_field)+"</p>"

          notification = Notification()
          notification.receiver = item.owner
          notification.notification_type = "MATCH"
          notification.message = "This item matched your lost "
          notification.topic = match.object
          notification.match = item
          notification.save()
         
          log += "<p>== Notification Created</p>"
          log += "<p>=======================</p>"
    log += "<p><p>========= END JOB =======</p>"
    log += "<p>=========================</p>"

  except Exception, e:
      traceback.print_exc()

  return HttpResponse(log)

def save_base64image_to_media(media_obj, data):
  img_temp = NamedTemporaryFile()
  img_temp.write(base64.b64decode(data))
  img_temp.flush()
  media_obj.data.save("media.jpg", File(img_temp))
