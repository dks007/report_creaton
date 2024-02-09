"""
    permissions file
"""
import os

from rest_framework import permissions


class IFSPermission(permissions.BasePermission):
    """
    to check if resource is active
    """

    def has_permission(self, request, view):
        """ return True if token resource is active"""
        if request.auth.payload.get('appid') == os.getenv('LOGIN_APP_ID'):
            return True
        return False
