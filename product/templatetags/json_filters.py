from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(str(key), '')

@register.filter
def to_range(value):
    """Converts an integer to a range object for looping."""
    return range(value)