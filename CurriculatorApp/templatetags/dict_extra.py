from django import template
import json

register = template.Library()

@register.filter(name="dict_to_json")
def dict_to_json(value):
    return json.dumps(value)

