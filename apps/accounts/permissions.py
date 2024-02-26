import os
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

class IFSPermission(permissions.BasePermission):
    """
    Permission class to check if a resource is active.
    """

    def has_permission(self, request, view):
        """
        Check if the token resource is active.
        """
        try:
            token_appid = request.auth.payload.get('appid')
            login_app_id = os.getenv('LOGIN_APP_ID')
            
            if token_appid and token_appid == login_app_id:
                return True
            else:
                return False
        except Exception as e:
            # Log or handle the exception appropriately
            raise PermissionDenied("Error while checking resource activity: {}".format(str(e)))
