from django import template
import re

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(str(key), '')

@register.filter
def to_range(value):
    """Converts an integer to a range object for looping."""
    return range(value)

@register.filter
def spaced_model(value: str) -> str:
    """Pretty-print model code names like 'rawmaterialbatch' -> 'Rawmaterial Batch'."""
    if not value:
        return value
    text = str(value).strip().replace('_', ' ')
    text = re.sub(r'(batch)\b', r' \1', text, flags=re.IGNORECASE)
    text = re.sub(r'(test)\b', r' \1', text, flags=re.IGNORECASE)
    text = re.sub(r'\s{2,}', ' ', text)
    return ' '.join(p.capitalize() for p in text.split())