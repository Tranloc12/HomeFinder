from collections import defaultdict
from datetime import datetime

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncQuarter, TruncYear
from django.template.response import TemplateResponse
from django.utils.safestring import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.urls import path

from .models import User, Listing, Follow, Comment, Notification, ActivityLog


class CustomAdminSite(admin.AdminSite):
    site_header = 'HỆ THỐNG HỖ TRỢ TÌM KIẾM NHÀ TRỌ'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('user-stats/', self.admin_view(self.user_stats), name='user-stats'),
        ]
        return custom_urls + urls

    def user_stats(self, request):
        User = get_user_model()
        period = request.GET.get('period', 'month')
        month = request.GET.get('month')
        year = request.GET.get('year')
        quarter = request.GET.get('quarter')

        now = datetime.now()
        current_year = now.year

        if period == 'month':
            if month and year:
                user_stats = User.objects.filter(last_login__year=year, last_login__month=month) \
                    .annotate(period=TruncMonth('last_login')) \
                    .values('period', 'role') \
                    .annotate(count=Count('id'))
            else:
                user_stats = []

        elif period == 'quarter':
            if year and quarter:
                if quarter == '1':
                    months = [1, 2, 3]
                elif quarter == '2':
                    months = [4, 5, 6]
                elif quarter == '3':
                    months = [7, 8, 9]
                elif quarter == '4':
                    months = [10, 11, 12]
                else:
                    months = []

                user_stats = User.objects.filter(last_login__year=year, last_login__month__in=months) \
                    .annotate(period=TruncQuarter('last_login')) \
                    .values('period', 'role') \
                    .annotate(count=Count('id'))
            else:
                user_stats = []

        elif period == 'year':
            if year:
                user_stats = User.objects.filter(last_login__year=year) \
                    .annotate(period=TruncYear('last_login')) \
                    .values('period', 'role') \
                    .annotate(count=Count('id'))
            else:
                user_stats = []

        else:
            user_stats = []

        stats_by_role = defaultdict(list)
        for stat in user_stats:
            stats_by_role[stat['role']].append(stat)

        return TemplateResponse(request, 'admin/user_stats.html', {
            'user_stats': user_stats,
            'stats_by_role': stats_by_role,
            'current_year': current_year,
        })


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff')
    search_fields = ('email', 'username')
    list_filter = ('role', 'is_active', 'is_staff')
    readonly_fields = ['image']

    def image(self, User):
        if User.avatar:
            # Kiểm tra xem avatar có tồn tại và trả về URL từ Cloudinary
            return mark_safe(f"<img src='{User.avatar.url}' width='120' />")
        return None  # Nếu không có avatar, trả về None

    image.short_description = 'Avatar'  # Tên cột hiển thị trong Admin


class ListingForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Listing
        fields = '__all__'


class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'host', 'is_approved', 'is_verified')
    search_fields = ('title', 'address', 'district')
    list_filter = ('is_approved', 'is_verified', 'created_date')
    ordering = ('-created_date',)
    form = ListingForm
    readonly_fields = ['avatar']

    def avatar(self, Listing):
        if Listing:
            return mark_safe(f"<img src='/static/{Listing.image.name}' width='120' />")


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'host', 'created_date')
    search_fields = ('user__email', 'host__email')
    list_filter = ('created_date',)


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Comment
        fields = '__all__'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('listing', 'user', 'created_date')
    search_fields = ('listing__title', 'user__email', 'content')
    list_filter = ('created_date',)
    form = CommentForm


class NotificationForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Notification
        fields = '__all__'


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_date')
    search_fields = ('user__email', 'content')
    list_filter = ('created_date',)
    form = NotificationForm


class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp')
    search_fields = ('user__email', 'action')
    list_filter = ('timestamp',)


admin_site = CustomAdminSite(name='myadmin')
admin_site.register(User, UserAdmin)
admin_site.register(Listing, ListingAdmin)
admin_site.register(Comment, CommentAdmin)
admin_site.register(Follow, FollowAdmin)
admin_site.register(Notification, NotificationAdmin)
admin_site.register(ActivityLog, ActivityLogAdmin)
