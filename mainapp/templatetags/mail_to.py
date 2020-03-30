from xml.etree import ElementTree as ET

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name="mail_to")
def mail_to(input_str):
    """
    create link mailto:
    """
    link_mailto = ET.Element("a", {"href": f"mailto:{input_str}"})
    link_mailto.text = input_str

    return mark_safe(ET.tostring(link_mailto, encoding="unicode"))
