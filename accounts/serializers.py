from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from .models import User
import uuid
from django.utils import timezone
from datetime import timedelta


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'full_name', 'phone_number', 'password', 'password2')
    
    def validate(self, attrs):
        """Validate that passwords match"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                'password': 'Passwords do not match.'
            })
        return attrs
    
    def create(self, validated_data):
        """Create a new user with encrypted password"""
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    
    def validate(self, attrs):
        """Authenticate user credentials"""
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials.')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Both username and password are required.')
        
        return attrs


class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer for user detail"""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'full_name', 'phone_number', 'profile_picture', 'created_at')
        read_only_fields = ('id', 'created_at')


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for user profile update"""
    class Meta:
        model = User
        fields = ('full_name', 'phone_number', 'profile_picture')


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing password"""
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    new_password2 = serializers.CharField(write_only=True, required=True)
    
    def validate(self, attrs):
        """Validate passwords"""
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({
                'new_password': 'New passwords do not match.'
            })
        return attrs


class PasswordResetRequestSerializer(serializers.Serializer):
    """Serializer for requesting password reset"""
    email = serializers.EmailField(required=True)


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Serializer for confirming password reset"""
    token = serializers.UUIDField(required=True)
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    new_password2 = serializers.CharField(write_only=True, required=True)
    
    def validate(self, attrs):
        """Validate passwords"""
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({
                'new_password': 'New passwords do not match.'
            })
        return attrs
