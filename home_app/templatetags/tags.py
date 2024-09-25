from django import template


register = template.Library()


@register.simple_tag
def time_zone():
    pass
