#### Adapted from http://stackoverflow.com/questions/13376576/how-can-i-use-a-variable-as-index-in-django-template ####
from django import template


register = template.Library()


@register.filter
def get_notifications(list, index):
    try:
        return list[index]
    except:
        return None