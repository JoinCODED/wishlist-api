from pkgutil import iter_modules
from rest_framework import permissions
from items.models import Item

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)

class IsAdminOrOwnerCanView(permissions.BasePermission):
    def has_permission(self, request, view):
        itemId = request.parser_context['kwargs'].get('pk')
        if itemId != None:
            itemFound = Item.objects.get(id = itemId)
            if itemFound:

                # itemIs = Item.objects.get(added_by_id = request.user.id)
                # print(request.parser_context['kwargs'].get('pk'))
                # print(itemFound.added_by.id == request.user.id)
                return bool(request.user and (request.user.is_staff or itemFound.added_by.id == request.user.id))
        return bool(request.user and request.user.is_staff)
