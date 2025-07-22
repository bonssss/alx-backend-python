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
    Permission to allow only authenticated users who are participants
    of the conversation to access and modify messages.
    """

    def has_permission(self, request, view):
        # Ensure user is authenticated
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # Assuming 'obj' can be either a Conversation or Message instance
        # and both have a 'participants' ManyToMany or a similar field

        # If obj is a message, get its conversation participants
        if hasattr(obj, 'conversation'):
            participants = obj.conversation.participants.all()
        elif hasattr(obj, 'participants'):
            participants = obj.participants.all()
        else:
            # fallback: if no participants info, deny access
            return False

        return request.user in participants