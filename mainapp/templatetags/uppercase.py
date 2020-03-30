from django import template

register = template.Library()

@register.filter(name='uppercase')
def uppercase(input_str):
    return input_str.upper()