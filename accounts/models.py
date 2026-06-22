import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone

class User(AbstractUser):
        full_name = models.CharField(max_length=100)
        email = models.EmailField(unique=True)
        phone_number = models.CharField(max_length=15, blank=True)
        profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def __str__(self):
            return self.username

class Folder(models.Model):
        owner = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            related_name='folders'
        )
        name = models.CharField(max_length=255)
        parent = models.ForeignKey(
            'self',
            on_delete=models.CASCADE,
            null=True, blank=True,
            related_name='subfolders'
        )
        created_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return self.name


class File(models.Model):
        owner = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            related_name='files'
        )
        folder = models.ForeignKey(
            Folder,
            on_delete=models.SET_NULL,
            null=True, blank=True,
            related_name='files'
        )
        file_name = models.CharField(max_length=255)
        file = models.FileField(upload_to='encrypted_files/')
        file_size = models.BigIntegerField()
        encrypted_key = models.TextField()
        is_encrypted = models.BooleanField(default=True)
        uploaded_at = models.DateTimeField(auto_now_add=True)
        sha256_hash=models.CharField(max_length=64,blank=True,default="")
        Encyrption_choices=(
              ('AES256','AES-256'),
              ('Dual','Dual Layer Encryption'),
        )
        encryption_type=models.CharField(max_length=20,choices=Encyrption_choices,default='AES256')

        def __str__(self):
            return self.file_name

class SharedFile(models.Model):
        PERMISSION_CHOICES = [
            ('view', 'View'),
            ('download', 'Download'),
        ]

        file = models.ForeignKey(File, on_delete=models.CASCADE, related_name='shares')
        shared_by = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            related_name='shared_files_sent'
        )
        shared_with = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            null=True, blank=True,       # null = public link share
            related_name='shared_files_received'
        )
        permission = models.CharField(max_length=20, choices=PERMISSION_CHOICES, default='view')
        share_token = models.UUIDField(default=uuid.uuid4, unique=True)   # for shareable link
        share_password = models.CharField(max_length=255, blank=True, null=True)  # store hashed
        expires_at = models.DateTimeField(null=True, blank=True)
        shared_at = models.DateTimeField(auto_now_add=True)
        max_downloads = models.PositiveIntegerField(default=1)
        current_downloads = models.PositiveIntegerField(default=0)
        is_active = models.BooleanField(default=True)

class Downloading(models.Model):
        share=models.ForeignKey(SharedFile,on_delete=models.CASCADE)
        user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
        ip_address=models.GenericIPAddressField()
        downloaded_at=models.DateTimeField(auto_now_add=True)
class EmailVerificationToken(models.Model):
        user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='verification_tokens')
        tokens=models.UUIDField(default=uuid.uuid4,unique=True)
        expires_at=models.DateTimeField()
        is_used=models.BooleanField(default=False)
        created_at=models.DateTimeField(auto_now_add=True)
        def is_expired(self):
            return timezone.now() > self.expires_at
        def __str__(self):
            return f"Verification token for {self.user.username}"
