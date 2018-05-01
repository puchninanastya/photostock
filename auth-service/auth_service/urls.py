from django.urls import re_path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'profiles', views.ProfileViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    re_path(r'^', include(router.urls)),
    re_path(r'^user-token/check$', views.UserTokenCheckView.as_view(), name='check-user-token'),
    re_path(r'^user-token/$', views.UserTokenView.as_view(), name='create-user-token'),
    re_path(r'^app-token/$', views.AppTokenView.as_view(), name='create-app-token'),
]