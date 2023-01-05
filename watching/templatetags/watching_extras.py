from django import template

register = template.Library()

@register.filter(name='get_pic')
def get_pic(path):
    url = 'https://image.tmdb.org/t/p/w185' + path
    return url

@register.filter(name='get_value')
def get_value(dictionary, key):
    return dictionary.get(key)

@register.filter(name='index')
def index(indexable, i):
    return indexable[i]