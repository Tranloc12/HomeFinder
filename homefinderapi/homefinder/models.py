from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField


class UserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('Vui lòng điền tên người dùng (username).')
        if not email:
            raise ValueError('Vui lòng điền email.')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser phải có is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser phải có is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLES = [
        ('admin', 'Administrator'),
        ('host', 'Host'),
        ('tenant', 'Tenant'),
    ]

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    avatar = CloudinaryField('avatar', null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLES, default='tenant')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Listing(BaseModel):
    title = models.CharField(max_length=255)
    description = RichTextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=255)
    district = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    max_occupants = models.IntegerField(default=1)
    longitude = models.FloatField()
    latitude = models.FloatField()
    images = CloudinaryField('images', null=True, blank=True)
    host = models.ForeignKey(User, related_name='listings', on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Follow(BaseModel):
    user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    host = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)


class Comment(BaseModel):
    listing = models.ForeignKey(Listing, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    content = RichTextField()

    def __str__(self):
        return f"{self.user.username} - {self.listing.title}"


class RoomRequest(BaseModel):
    tenant = models.ForeignKey(User, related_name='room_requests', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = RichTextField()
    price_range = models.CharField(max_length=50)  # Ví dụ: "2tr-3tr"
    preferred_location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)  # Thêm trường này nếu chưa có.

    def __str__(self):
        return self.title


class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, null=True, blank=True, on_delete=models.CASCADE)
    room_request = models.ForeignKey(RoomRequest, null=True, blank=True, on_delete=models.CASCADE)
    content = models.TextField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[:20]



class Notification(BaseModel):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"Notification for {self.user.username}"


class Chat(BaseModel):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat from {self.sender.username} to {self.receiver.username}"


class Statistics(BaseModel):
    date = models.DateField()
    total_users = models.IntegerField()
    total_hosts = models.IntegerField()
    total_listings = models.IntegerField()

    def __str__(self):
        return f"Statistics for {self.date}"


