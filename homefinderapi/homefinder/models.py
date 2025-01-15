from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from ckeditor.fields import RichTextField

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
    avatar = models.ImageField(upload_to='avatars/%Y/%m/', blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLES, default='tenant')
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
    max_occupants = models.IntegerField(default=1)
    longitude = models.FloatField()
    latitude = models.FloatField()
    image = models.ImageField(upload_to='listings/%Y/%m/')
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


class Notification(BaseModel):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    content = RichTextField()


class ActivityLog(BaseModel):
    user = models.ForeignKey(User, related_name='activity_logs', on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
