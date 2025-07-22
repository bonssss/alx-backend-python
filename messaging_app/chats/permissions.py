from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Custom permission to allow only owners of an object to access it.
    """

    def has_object_permission(self, request, view, obj):
        # Adjust 'user' field name as per your model
        return obj.user == request.user
