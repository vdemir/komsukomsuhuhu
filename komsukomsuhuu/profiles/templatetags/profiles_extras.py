__author__ = 'havvafeyzamete'
from django import template

register = template.Library()

@register.filter(name='subs')
def subs(value, arg):
    return abs(value-arg)