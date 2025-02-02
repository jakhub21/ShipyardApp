from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Zwraca wartość ze słownika na podstawie podanego klucza"""
    return dictionary.get(key, {})

@register.filter
def dict_key(d, key):
    return d.get(key, {})
