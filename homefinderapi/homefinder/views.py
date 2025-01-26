from pickle import FALSE

from django.contrib.admin.templatetags.admin_list import pagination
from oauth2_provider.contrib.rest_framework import permissions
from rest_framework import viewsets, generics, serializers
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from . import paginators
from .models import User, Listing, Follow, Comment, Notification, RoomRequest, Chat, Statistics
from .serializers import UserSerializer, ListingSerializer, FollowSerializer, CommentSerializer, NotificationSerializer, \
    RoomRequestSerializer, ChatSerializer, StatisticsSerializer


# User ViewSet
class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    pagination_class = paginators.ItemPaginator
    parser_classes = [MultiPartParser, FormParser]

    @action(methods=['get'], url_path='current-user', detail=False, permission_classes=[permissions.IsAuthenticated])
    def get_user(self, request):
        return Response(UserSerializer(request.user).data)

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

# Chat ViewSet
class ChatViewSet(viewsets.ViewSet, generics.ListCreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = paginators.ItemPaginator

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


# RoomRequest ViewSet
class RoomRequestViewSet(viewsets.ViewSet, generics.ListCreateAPIView):
    queryset = RoomRequest.objects.all()
    serializer_class = RoomRequestSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = paginators.ItemPaginator

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user)


class StatisticsViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Statistics.objects.all()  # Trả về tất cả các bản ghi Statistics
    serializer_class = StatisticsSerializer  # Sử dụng StatisticsSerializer cho các response

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user)