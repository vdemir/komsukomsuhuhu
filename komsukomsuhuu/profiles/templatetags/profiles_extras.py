__author__ = 'havvafeyzamete'
from django import template

register = template.Library()

@register.filter(name='subs')
def subs(value, arg):
    return abs(value-arg)


@register.filter(name='get_range')
def get_range(value):
    return range(1, value+1)