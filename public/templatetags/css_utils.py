from django import template
from django.core.serializers import serialize
from django.db.models.query import QuerySet
import json
register = template.Library()

@register.filter(name='addcss')
def addcss(field, css):
	attrs = {}
	definition = css.split(',')

	for d in definition:
		t, v = d.split(':')
		attrs[t] = v

	return field.as_widget(attrs=attrs)

@register.filter(name='jsonify')
def jsonify(object):
	if isinstance(object, QuerySet):
	    return serialize('json', object)
	return json.dumps(object)