from django.shortcuts import redirect

from social.pipeline.partial import partial

USER_FIELDS = ['username', 'email']

@partial
def require_email(strategy, details, user=None, is_new=False, *args, **kwargs):
    if kwargs.get('ajax') or user and user.email:
        return
    elif is_new and not details.get('email'):
        email = strategy.request_data().get('email')
        if email:
            details['email'] = email
        else:
            return redirect('public:require_email')

@partial
def user_details(strategy, details, response, user=None, *args, **kwargs):
	if user:
	  if kwargs['is_new']:
		user.is_active = True
		user.save()