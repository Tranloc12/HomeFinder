from django.contrib.admin.templatetags.admin_list import pagination
from rest_framework import viewsets, generics, serializers
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from . import paginators
from .models import User, Listing, Follow, Comment, Notification, ActivityLog
from .serializers import UserSerializer, ListingSerializer, FollowSerializer, CommentSerializer, NotificationSerializer, ActivityLogSerializer

# User ViewSet
class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]  # Chỉ cho phép người dùng đã xác thực truy cập
    pagination_class = paginators.ItemPaginator
    parser_classes = [MultiPartParser, FormParser]


# Listing ViewSet
class ListingViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = paginators.ItemPaginator

    @action(methods=['get'], url_path='comments', detail=True)
    def get_comment(self, request, pk):
        comments = self.get_object().comments.select_related('user').filter(active=True)
        return Response(CommentSerializer(comments, many=True).data)

    def perform_create(self, serializer):
        # Khi tạo mới Listing, đảm bảo rằng host là người dùng đang đăng nhập
        serializer.save(host=self.request.user)

    def get_queryset(self):
        query=self.queryset

        kw=self.request.query_params.get('q')
        if kw:
            query=query.filter(title__icontains=kw)

        return query


# Follow ViewSet
class FollowViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = paginators.ItemPaginator

    def perform_create(self, serializer):
        # Khi tạo mới Follow, đảm bảo rằng user đang theo dõi là người dùng đang đăng nhập
        serializer.save(user=self.request.user)


# Comment ViewSet
class CommentViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = paginators.ItemPaginator

    def perform_create(self, serializer):
        # Khi tạo mới Comment, đảm bảo rằng user là người dùng đang đăng nhập
        serializer.save(user=self.request.user)


# Notification ViewSet
class NotificationViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = paginators.ItemPaginator

    def perform_create(self, serializer):
        # Khi tạo mới Notification, đảm bảo rằng user là người dùng đang đăng nhập
        serializer.save(user=self.request.user)


# ActivityLog ViewSet
class ActivityLogViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = paginators.ItemPaginator

    def perform_create(self, serializer):
        # Khi tạo mới ActivityLog, đảm bảo rằng user là người dùng đang đăng nhập
        serializer.save(user=self.request.user)
