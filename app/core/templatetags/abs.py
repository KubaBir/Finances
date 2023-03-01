from django import template

register = template.Library()


@register.filter(name='abs')
def abs(value):
    # value = float(value)
    # if value >= 0:
    #     return value
    # return -value
    return value
