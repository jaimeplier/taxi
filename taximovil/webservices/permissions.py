from rest_framework import permissions


class ChoferPermission(permissions.BasePermission):
    """
    Permisos del chofer
    Rol:
    superuser: 1
    chofer: 3
    callcenter: 12
    """

    def has_permission(self, request, view):
        if request.user is not None:
            return request.user.rol.pk == 3 or request.user.rol.pk == 1 or request.user.rol.pk == 12
        return False


class CallcenterPermission(permissions.BasePermission):
    """
    Permisos del chofer
    Rol:
    superuser: 1
    administrador: 9
    callcenter: 12
    """

    def has_permission(self, request, view):
        if request.user is not None:
            return request.user.rol.pk == 1 or request.user.rol.pk == 9 or request.user.rol.pk == 12
        return False


class AdministradorPermission(permissions.BasePermission):
    """
    Permisos del administrador
    Rol:
    superuser: 1
    administrador: 9
    """

    def has_permission(self, request, view):
        if request.user is not None:
            return request.user.rol.pk == 9 or request.user.rol.pk == 1
        return False


class AdministradorSitioPermission(permissions.BasePermission):
    """
    Permisos del administrador
    Rol:
    superuser: 1
    administrador: 9
    administrador de ciudad 5
    administrador de sitio 10
    """

    def has_permission(self, request, view):
        if request.user is not None:
            return request.user.rol.pk == 9 or request.user.rol.pk == 1 or request.user.rol.pk == 10 or request.user.rol.pk == 5
        return False


class AdministradorCiudadPermission(permissions.BasePermission):
    """
    Permisos del administrador
    Rol:
    superuser: 1
    administrador: 9
    administrador de ciudad 5
    """

    def has_permission(self, request, view):
        if request.user is not None:
            return request.user.rol.pk == 9 or request.user.rol.pk == 1 or request.user.rol.pk == 5
        return False


class IsOwnerPermission(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.rol.pk == 2:
            return obj.cliente.pk == request.user.pk
        elif request.user.rol.pk == 3:
            return obj.chofer.pk == request.user.pk
        elif request.user.rol.pk == 1:
            return True
        return False
