from django import template
register = template.Library()


@register.filter
def get_mod(arg1, arg2):
    return arg1 % int(arg2) + 1