from django import template
from app.models import *


register = template.Library()

@register.simple_tag
def hasPermission(user):
	# if user.is_superuser:
	# 	return True
	permissions = userPermission.objects.filter(user_id=user.id).first()
	return permissions;
	# if permissions:
	# 	userPermissions = permissions
	# 	return True	
	# 	if userPermissions:
	# 		if permissionGiven in userPermissions:
	# 			return True

	# return False