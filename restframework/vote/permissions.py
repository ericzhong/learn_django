from rest_framework import permissions



class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:    # get,head,options
            return True

        return obj.create_by == request.user
