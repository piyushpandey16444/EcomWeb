from django import template
register = template.Library()


@register.simple_tag
def round_value(value):
    print(value)
    return round(value, 2)
    # return float('%.2f' % value)
