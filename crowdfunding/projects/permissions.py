# added to make custom permission that only the owner of a project can edit it
# inbuilt django 
from rest_framework import permissions


# Full access as owner or read only. 
class IsOwnerOrReadOnly(permissions.BasePermission):
    # DRF check for permissions 
    def has_object_permission(self, request, view, obj):
        # user can still access via safe actions such as get / head / options 
        if request.method in permissions.SAFE_METHODS:
            return True
            # if conditions are met where they are the owner & the rqst user they can put / post / delete
        return obj.owner == request.user


# Only the profile owner can view profile . 
class IsOwnProfile(permissions.BasePermission):
    # DRF check for permissions 
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
            # if conditions are met where they are the profile owner & the rqst user they can put / post / delete
        return obj.id == request.user.id


# Full access as supporter owner or read only. 
class IsSupporterOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
        # if conditions are met where they are the owner & the rqst user they can put / post / delete, else read only 
            return True
        return obj.supporter == request.user

# Full access as comment owner or read only. 
class IsCommentatorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
        # if conditions are met where they are the owner & the rqst user they can put / post / delete, else read only 
            return True
        return obj.commentator == request.user
