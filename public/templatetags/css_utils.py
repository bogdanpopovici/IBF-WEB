from django import template
register = template.Library()

@register.filter(name='addcss')
def addcss(field, css):
	attrs = {}
	definition = css.split(',')

	for d in definition:
		t, v = d.split(':')
		attrs[t] = v

	return field.as_widget(attrs=attrs)