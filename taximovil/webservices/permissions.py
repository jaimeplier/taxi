from rest_framework import permissions


class ProfesorPermission(permissions.BasePermission):
    """
    Permisos del chofer
    Rol:
    superuser: 1
    chofer: 3
    """
    def has_permission(self, request, view):
        if request.user is not None:
            return request.user.rol.pk == 3 or request.user.rol.pk == 1
        return False