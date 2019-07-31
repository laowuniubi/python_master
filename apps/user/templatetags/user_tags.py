from django import template
from django.utils.functional import SimpleLazyObject

# 自定义的过滤器，用于过滤request.user


register = template.Library()


@register.filter  # 将过滤器注册到系统中
def is_user(user):
    if user.id is None:
        return None
    if user.name is None:
        return None
    return user