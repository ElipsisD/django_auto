import locale

from django import template

register = template.Library()

@register.filter
def thousands(value):
    """Разделение числа на разряды."""
    return locale.format_string("%d", value, grouping=True)
