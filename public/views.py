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


def index(request):

  error = ''
  notifications = []
  matches = []

  if request.method=='POST':
    username = request.POST['username']
    password = request.POST['password']
    

    user = authenticate(username=username, password=password)
    if user is not None:
      if user.is_active:
        login(request, user)
      else:
        error="The account you are trying to access has been disabled. Please contact the website's administrator."
    else:
        error="Your username and password didn't match. Please try again."

  if request.user and request.user.is_authenticated():
    notifications = Notification.objects.filter(receiver=request.user, seen=False, notification_type__in=['CLAIM','ACCEPT'])
    matches = Notification.objects.filter(receiver=request.user, seen=False, notification_type="MATCH")
  context = RequestContext(request,
                           {'request': request,
                            'user': request.user,
                            'notifications': notifications,
                            'matches': matches,
                            'error_message': error,
                            'MEDIA_URL': MEDIA_URL
                            })
  return render_to_response('public/home.html', context_instance=context)

def register(request):
  if request.method == 'POST':
      form = RegistrationForm(request.POST)
      if form.is_valid():
          new_user = form.save()
          username = new_user.username
          email = new_user.email
          password = request.POST['password1']
          

          salt = hashlib.sha1(str(random.random())).hexdigest()[:5]            
          activation_key = hashlib.sha1(salt+email).hexdigest()            
          key_expires = datetime.datetime.today() + datetime.timedelta(2)

          #Get user by username
          user=get_user_model().objects.get(username=username)

          # Create and save user profile                                                                                                                                  
          new_profile = UserProfile(user=user, activation_key=activation_key, 
              key_expires=key_expires)
          new_profile.save()

          # Send email with activation key
          email_subject = 'Account confirmation'
          email_body = "Hey %s, thanks for signing up. To activate your account, click this link within \
          48hours http://ibf.herokuapp.com//accounts/confirm/%s" % (username, activation_key)

          send_mail(email_subject, email_body, 'myemail@example.com',
              [email], fail_silently=False)

          context = RequestContext(request,
                           {'request': request,
                            'user': request.user,
                            'email': email
                            })

          return render_to_response('public/confirm_sent.html', context_instance=context)
      else:
        print "Invalid"
  context = RequestContext(request,
                           {'request': request,
                            'user': request.user
                            })
  return render_to_response('public/registration_form.html', context_instance=context)
  
def register_confirm(request, activation_key):

    if request.user.is_authenticated():
        HttpResponseRedirect('/')

    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)

    if user_profile.key_expires < timezone.now():
        return render_to_response('public/confirm_expired.html')

    user = user_profile.user
    user.is_active = True
    user.save()
    return render_to_response('public/confirm.html')

def context(**extra):
    return dict({
        'plus_id': getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None),
        'plus_scope': ' '.join(GooglePlusAuth.DEFAULT_SCOPE),
        'available_backends': load_backends(settings.AUTHENTICATION_BACKENDS)
    }, **extra)

@render_to('public/home.html')
def validation_sent(request):
    return context(
        validation_sent=True,
        email=request.session.get('email_validation_address')
    )


@render_to('public/home.html')
def require_email(request):
  context = RequestContext(request,
                           {'request': request,
                            'user': request.user,
                            'backend': request.session['partial_pipeline']['backend'],
                            'email_required': True
                            })
  return render_to_response('public/require_email.html', context_instance=context)


@psa('social:complete')
def ajax_auth(request, backend):
    if isinstance(request.backend, BaseOAuth1):
        token = {
            'oauth_token': request.REQUEST.get('access_token'),
            'oauth_token_secret': request.REQUEST.get('access_token_secret'),
        }
    elif isinstance(request.backend, BaseOAuth2):
        token = request.REQUEST.get('access_token')
    else:
        raise HttpResponseBadRequest('Wrong backend type')
    user = request.backend.do_auth(token, ajax=True)
    login(request, user)
    data = {'id': user.id, 'username': user.username}
    return HttpResponse(json.dumps(data), mimetype='application/json')

@login_required
def myaccount(request, **tab):

  user = request.user
  if not tab:
    tab = {'tab':1}
  #==========fetch user notifications==============
  message_sequences = []
  matches = []
  notifications= list(chain(Notification.objects.filter(sender=user), Notification.objects.filter(receiver=user)))
  messages = [x for x in notifications if x.notification_type == "CLAIM" or x.notification_type == "ACCEPT"]

  matches = [x for x in notifications if x.notification_type == "MATCH"]
  for macth in matches:
    media = Media.objects.all().filter(of_item=macth.topic)
    if media:
       macth.media = media[0]  

  groups= defaultdict( list )
  for obj in messages:
      if not obj.sender == user:
        obj.seen = True
        obj.save()
      groups[obj.topic].append( obj )
  groups_list = groups.values()
  index = 0
  for topic in groups_list:
    topic = sorted(topic, key=lambda x: x.created_at, reverse=False)
    for message in topic:
      if message.sender == user:
        message.type = 'SEND'
        other_user = message.receiver.username
      else:
        message.type = 'RECEIVE'
        other_user = message.sender.username
    message_sequence = {}
    message_sequence['messages'] = topic
    message_sequence['other_user'] = other_user
    message_sequence['index'] = index
    message_sequence['topic'] = topic[0]
    index += 1
    message_sequences.append(message_sequence)
  #==================================================

  #=========fetch pre-registered items===============
  pre_reg_items = PreRegisteredItem.objects.filter(owner=user)
  for item in pre_reg_items:
      media = Media.objects.all().filter(of_item=item)
      if media:
         item.media = media[0] 

  #=========fetch found items===============
  found_items = Item.objects.filter(found_by_user=user)
  for item in found_items:
      media = Media.objects.all().filter(of_item=item)
      if media:
         item.media = media[0]   

  context = RequestContext(request,
                           {'request': request,
                            'user': user,
                            'message_sequences':message_sequences,
                            'pre_reg_items': pre_reg_items,
                            'matches': matches,
                            'found_items': found_items,
                            'tab': tab['tab'],
                            'MEDIA_URL': MEDIA_URL
                            })
  return render_to_response('public/myaccount.html', context_instance=context)

@login_required
def edit_personal_details(request):
  
  user = request.user
  response_data = {}

  attr =  request.POST.get('field')
  value = request.POST.get('value')

  try:
    if (attr == 'first_name'):
      if not value:
        response_data['result'] = 'ERROR'
        response_data['err_message'] = 'First name must not be empty'
      else:
        response_data['result'] = 'OK'
        user.first_name = value
        user.save()
        response_data['new_value'] = value
    elif (attr == 'last_name'):
      if not value:
        response_data['result'] = 'ERROR'
        response_data['err_message'] = 'Last name must not be empty'
      else:
        response_data['result'] = 'OK'
        user.last_name = value
        user.save()
        response_data['new_value'] = value
    elif (attr == 'phone_number'):
      pattern = re.compile("\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}")
      if not pattern.match(value):  
        print value+"a"
        response_data['result'] = 'ERROR'
        response_data['err_message'] = 'Telephone number is not recognised'
      else:
        response_data['result'] = 'OK'
        user.phone_number = value
        user.save()
        response_data['new_value'] = value
    elif (attr == 'address'):
      response_data['result'] = 'OK'
      user.address = value
      user.save()
      response_data['new_value'] = value
    elif (attr == 'password'):
      current_password = request.POST.get('value1')
      new_password = request.POST.get('value2')
      confirm_password = request.POST.get('value3')

      if not request.user.check_password(current_password):
        response_data['result'] = 'ERROR'
        response_data['err_message'] = 'Old password is not correct'
      elif not new_password==confirm_password:
        response_data['result'] = 'ERROR'
        response_data['err_message'] = 'New password and confirmation password did not match'
      else:
        request.user.set_password(new_password)
        response_data['result'] = 'OK'
    elif (attr == 'email'):
      current_email = request.POST.get('value1')
      new_email = request.POST.get('value2')
      confirm_email = request.POST.get('value3')

      if not request.user.email == current_email:
        response_data['result'] = 'ERROR'
        response_data['err_message'] = 'Old email is not correct'
      elif not new_email==confirm_email:
        response_data['result'] = 'ERROR'
        response_data['err_message'] = 'New email and confirmation email did not match'
      else:
        request.user.email  = new_email
        request.user.save()
        response_data['result'] = 'OK'
        response_data['new_value'] = new_email
  except Exception, e:
    traceback.print_exc()
  else:
    pass
  finally:
    pass
  
  return HttpResponse(json.dumps(response_data), content_type="application/json")

def item_registration(request):

  if request.method=='POST':
    try:
     uid = request.POST.get('uniqueid')
     title = request.POST.get('title')
     category = request.POST.get('category')
     description = request.POST.get('description')
     tags = request.POST.get('tags')
     location = request.POST.get('location')
     photos = json.loads(request.POST['media'])
     new_item = Item()
     new_item.title = title
     new_item.unique_id = uid
     new_item.tags = tags
     new_item.description = description
     new_item.location = request.POST.get('location')
     new_item.category = category
     new_item.date_field = datetime.datetime.now().strftime("%Y-%m-%d")
     new_item.time_field = datetime.datetime.now().strftime("%H:%M:%S") 
     new_item.found_by_user = request.user
     new_item.save()

     for media in photos:
       photo = Media()
       photo.of_item = new_item
       photo.media_type = "PHOTO" 
       save_base64image_to_media(photo, media)
       photo.save()

     call_command('update_index')
     
     return HttpResponse(json.dumps({'result': 'OK'}), content_type="application/json")
    except Exception as e:
     traceback.print_exc()
     return HttpResponse(json.dumps({'result': 'ERROR'}), content_type="application/json")
  context = RequestContext(request,
                           {'request': request,
                            'user': request.user
                            })
  return render_to_response('public/registerfounditem.html', context_instance=context)

def save_base64image_to_media(media_obj, data):
  img_temp = NamedTemporaryFile()
  img_temp.write(base64.b64decode(data))
  img_temp.flush()
  media_obj.data.save("media.jpg", File(img_temp))
