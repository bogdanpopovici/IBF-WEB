from django import template
from django.core.serializers import serialize
from django.db.models.query import QuerySet
import json
register = template.Library()

@register.filter(name='addcss')
def addcss(field, css):
   return field.as_widget(attrs={"class":css})

@register.filter(name='jsonify')
def jsonify(object):
	if isinstance(object, QuerySet):
	    return serialize('json', object)
	return json.dumps(object)