from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, obj):
        return request.user == obj.user or request.user.is_staff or request.user.is_superuser