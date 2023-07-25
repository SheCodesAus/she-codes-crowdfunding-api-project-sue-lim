from .views import custom404
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

# custom 404 error message 
handler404 = custom404
# handler500 = custom500

# end points 
urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('', include('projects.urls')),  # getting access to project urls
    path('users/', include('users.urls')),
    path('api-auth/', include('rest_framework.urls')),  # adds login button
    path('api-token-auth/', obtain_auth_token,
         name='api_token_auth')  # adds generate token url


]
