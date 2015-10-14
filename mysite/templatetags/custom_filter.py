__author__ = 'linbingchen'
from django import template
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