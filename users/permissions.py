from rest_framework import permissions


class IsModer(permissions.BasePermission):
    message = "Только модераторы могут просматривать данный объект."

    def has_permission(self, request, view):
        if request.user.groups.filter(name="moderator").exists():
            return True
        else:
            return False
