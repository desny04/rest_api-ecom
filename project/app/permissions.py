from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsStaffOrReadOnly(BasePermission):
    def has_permission(self,request,view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)

class isAuthenticatedForDetail(BasePermission):
    def has_object_permission(self,request,view,obj):
        if view.action=='retrieve':
            return bool(request.user and request.user.is_authenticated)
        return True