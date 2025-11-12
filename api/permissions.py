from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Listing


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        member = getattr(request, "member", None)
        return getattr(obj, "author_id", None) == getattr(member, "id", None)
