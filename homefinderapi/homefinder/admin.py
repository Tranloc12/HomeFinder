from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import User, Listing, Follow, Comment, Notification, ActivityLog
from django import forms
from ckeditor_uploader.widgets \
import CKEditorUploadingWidget


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff')
    search_fields = ('email', 'username')
    list_filter = ('role', 'is_active', 'is_staff')

    readonly_fields = ['image']

    def image(self, User):
        if User:
            return mark_safe(f"<img src='/static/{User.avatar.name}' width='120' />")


class ListingForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Listing
        fields = '__all__'


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'host', 'is_approved', 'is_verified')
    search_fields = ('title', 'address', 'district')
    list_filter = ('is_approved', 'is_verified', 'created_date')
    ordering = ('-created_date',)
    form=ListingForm
    readonly_fields = ['avatar']

    def avatar(self, Listing):
        if Listing:
            return mark_safe(f"<img src='/static/{Listing.image.name}' width='120' />")


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'host', 'created_date')
    search_fields = ('user__email', 'host__email')
    list_filter = ('created_date',)


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Comment
        fields = '__all__'


@admin.register(Comment)
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


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_date')
    search_fields = ('user__email', 'content')
    list_filter = ('created_date',)
    form = NotificationForm


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp')
    search_fields = ('user__email', 'action')
    list_filter = ('timestamp',)
