from django import template
from recommend.crop_info import get_crop_data as fetch_crop_data

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter(name='add_percent_offset')
def add_percent_offset(total_stroke, percent):
    """Calculates SVG stroke-dashoffset for circular progress."""
    try:
        offset = float(total_stroke) - (float(total_stroke) * (float(percent) / 100))
        return offset
    except (ValueError, TypeError):
        return total_stroke

@register.filter(name='format_currency')
def format_currency(value):
    try:
        return "{:,.2f}".format(float(value))
    except (ValueError, TypeError):
        return value

@register.filter(name='get_crop_data')
def get_crop_data(name):
    """Fetches detailed crop metadata for template rendering."""
    return fetch_crop_data(name)
