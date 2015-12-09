__author__ = 'linbingchen'
from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
import re
register = template.Library()



@register.filter
def div( value, arg ):
    try:
        value = int( value )
        arg = int( arg )
        if arg:
            return 1.0 * value / arg
    except:
        pass
    return ''


@register.filter
def mult( value, arg ):
    try:
        value = int( value )
        arg = int( arg )
        if arg:
            return 1.0 * value * arg
    except:
        pass
    return ''

@register.filter
def spacify(value, autoescape=None):
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    return mark_safe(re.sub(' ', '&nbsp;', esc(value)))