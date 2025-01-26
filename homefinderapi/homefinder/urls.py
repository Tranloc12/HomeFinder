from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import UserViewSet, ListingViewSet, FollowViewSet, CommentViewSet, NotificationViewSet

# Khởi tạo DefaultRouter
router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'listings', views.ListingViewSet, basename='listing')
router.register(r'follow', views.FollowViewSet, basename='follow')
router.register(r'comments', views.CommentViewSet, basename='comment')
router.register(r'notifications', views.NotificationViewSet, basename='notification')
router.register(r'chats', views.ChatViewSet, basename='chat')
router.register(r'room_requests', views.RoomRequestViewSet, basename='roomrequest')
router.register(r'statistics', views.StatisticsViewSet, basename='statistics')

urlpatterns = [
    path('', include(router.urls)),
]
