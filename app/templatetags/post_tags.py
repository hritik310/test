from django import template
from app.models import *


register = template.Library()

@register.simple_tag
def has_permission(user,permission):
	return request.user,1