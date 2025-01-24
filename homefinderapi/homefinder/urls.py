from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import UserViewSet, ListingViewSet, FollowViewSet, CommentViewSet, NotificationViewSet, ActivityLogViewSet

# Khởi tạo DefaultRouter
router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'listings', views.ListingViewSet, basename='listing')
router.register(r'follow', views.FollowViewSet, basename='follow')
router.register(r'comments', views.CommentViewSet, basename='comment')
router.register(r'notifications', views.NotificationViewSet, basename='notification')
router.register(r'activity_logs', views.ActivityLogViewSet, basename='activitylog')

urlpatterns = [
    path('', include(router.urls)),
]
