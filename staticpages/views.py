#  --- University of Southampton ---
#  --- Group Design Project in collaboration with 'The Big Consulting' ---
#  --- Copyright 2015 ---

from django.shortcuts import render_to_response
from django.template.context import RequestContext

def contact_page(request):
  context = RequestContext(request,
                           {'request': request,
                            'user': request.user
                            })
  return render_to_response('staticpages/contact_page.html', context_instance=context)

def terms_conditions(request):
  context = RequestContext(request,
                           {'request': request,
                            'user': request.user
                            })
  return render_to_response('staticpages/terms_conditions.html', context_instance=context)

def accessibility_support(request):
  context = RequestContext(request,
                           {'request': request,
                            'user': request.user
                            })
  return render_to_response('staticpages/accessibility_support.html', context_instance=context)


def site_map(request):
  context = RequestContext(request,
                           {'request': request,
                            'user': request.user
                            })
  return render_to_response('staticpages/site_map.html', context_instance=context)


def about_us(request):
  context = RequestContext(request,
                           {'request': request,
                            'user': request.user
                            })
  return render_to_response('staticpages/about_us.html', context_instance=context)

def our_strategy(request):
  context = RequestContext(request,
                           {'request': request,
                            'user': request.user
                            })
  return render_to_response('staticpages/our_strategy.html', context_instance=context)

def why_our_services(request):
  context = RequestContext(request,
                           {'request': request,
                            'user': request.user
                            })
  return render_to_response('staticpages/why_our_services.html', context_instance=context)

def register_tutorial(request):
  context = RequestContext(request,
                           {'request': request,
                            'user': request.user
                            })
  return render_to_response('staticpages/register_tutorial.html', context_instance=context)

def search_tutorial(request):
  context = RequestContext(request,
                           {'request': request,
                            'user': request.user
                            })
  return render_to_response('staticpages/search_tutorial.html', context_instance=context)

def return_item(request):
  context = RequestContext(request,
                           {'request': request,
                            'user': request.user
                            })
  return render_to_response('staticpages/return_item.html', context_instance=context)

def common_tips(request):
  context = RequestContext(request,
                           {'request': request,
                            'user': request.user
                            })
  return render_to_response('staticpages/common_tips.html', context_instance=context)