from django import template

register = template.Library()

@register.filter
def remove(value, arg):
    for item in arg.split(','):
        value = value.replace(item, "")
    return value