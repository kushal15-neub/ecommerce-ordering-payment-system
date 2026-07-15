from rest_framework.permissions import BasePermission


class IsAdminUserRole(BasePermission):

    def has_permission(self, request, view):

        if request.method in [
            "GET",
            "HEAD",
            "OPTIONS"
        ]:
            return True

        return (
            request.user.is_authenticated
            and request.user.role == "admin"
        )