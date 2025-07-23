from rest_framework.permissions import BasePermission
from rest_framework import permissions

class IsOwner(BasePermission):
    """
    Custom permission to allow only owners of an object to access it.
    """

    def has_object_permission(self, request, view, obj):
        # Adjust 'user' field name as per your model
        return obj.user == request.user
class IsParticipantOfConversation(BasePermission):
    """
    Permission to allow only participants of the conversation
    to send, view, update, and delete messages.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Get participants depending on object type
        if hasattr(obj, 'participants'):
            participants = obj.participants.all()
        elif hasattr(obj, 'conversation'):
            participants = obj.conversation.participants.all()
        else:
            return False

        if request.method in SAFE_METHODS:
            # GET, HEAD, OPTIONS: allow if participant
            return request.user in participants
        elif request.method in ['PUT', 'PATCH', 'DELETE']:
            # Only allow if participant
            return request.user in participants
        else:
            # For other HTTP methods, deny by default
            return False