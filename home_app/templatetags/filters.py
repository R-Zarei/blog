from django import template


register = template.Library()


@register.filter(name='my_cut')
def cut(value, arg):
    try:
        arg = int(arg)
        return value[:arg]
    except IndexError:
        return ''
