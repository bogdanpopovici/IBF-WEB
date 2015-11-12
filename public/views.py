from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, get_object_or_404
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from social.backends.oauth import BaseOAuth1, BaseOAuth2
from social.backends.google import GooglePlusAuth
from social.backends.utils import load_backends
from social.apps.django_app.utils import psa
from public.decorators import render_to
from django.contrib.auth import get_user_model
from core.forms import RegistrationForm
from core.models import UserProfile
import hashlib, datetime, random, json, re, traceback
from django.core.mail import send_mail
from django.utils import timezone

def index(request):

  error = ''

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

  context = RequestContext(request,
                           {'request': request,
                            'user': request.user,
                            'error_message': error
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
          48hours http://127.0.0.1:8000/accounts/confirm/%s" % (username, activation_key)

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
  print "yes"
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
def myaccount(request):

  context = RequestContext(request,
                           {'request': request,
                            'user': request.user
                            })
  return render_to_response('public/myaccount.html', context_instance=context)

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
      pattern = re.compile("^d+$")
      if not pattern.match(value):  
        response_data['result'] = 'ERROR'
        response_data['err_message'] = 'Telephone number must contain only digits'
      else:
        response_data['result'] = 'OK'
        user.phone_number = value
        user.save()
        response_data['new_value'] = value
  except Exception, e:
    traceback.print_exc()
  else:
    pass
  finally:
    pass
  
  return HttpResponse(json.dumps(response_data), content_type="application/json")

def item_registration(request):
  context = RequestContext(request,
                           {'request': request,
                            'user': request.user
                            })
  return render_to_response('public/registerfounditem.html', context_instance=context)

#=============Implement search View Here====================

from haystack.generic_views import SearchView

RESULTS_PER_PAGE = getattr(settings, 'HAYSTACK_SEARCH_RESULTS_PER_PAGE', 20)


class CustomSearchView(SearchView):
    template = 'search/search.html'

