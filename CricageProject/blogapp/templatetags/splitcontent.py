from django import template
import copy

register = template.Library()


@register.filter
def split(content):
    content = content.replace("\r", "").split("\n", 7)
    ss = copy.deepcopy(content)
    l = 0
    for i, c in enumerate(content):
        if c == "":
            ss.pop(i - l)
            l += 1
    return ss
