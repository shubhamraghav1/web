from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User, PasswordResetToken, EmailVerificationToken


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'email', 'username', 'first_name', 'last_name', 
            'phone_number', 'date_of_birth', 'password', 'password_confirm'
        ]

    def validate(self, attrs):
        """Validate password confirmation"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs

    def validate_email(self, value):
        """Validate email uniqueness"""
        if User.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value.lower()

    def validate_username(self, value):
        """Validate username uniqueness"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value

    def create(self, validated_data):
        """Create new user with hashed password"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        """Authenticate user credentials"""
        email = attrs.get('email', '').lower()
        password = attrs.get('password', '')
        
        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                username=email,
                password=password
            )
            
            if not user:
                raise serializers.ValidationError("Invalid email or password.")
            
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled.")
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError("Must include email and password.")


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile (read/update)
    """
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name', 'full_name',
            'phone_number', 'date_of_birth', 'profile_picture', 'is_email_verified',
            'created_at', 'updated_at', 'last_login_at'
        ]
        read_only_fields = ['id', 'email', 'created_at', 'updated_at', 'is_email_verified']

    def validate_username(self, value):
        """Validate username uniqueness on update"""
        user = self.instance
        if user and User.objects.filter(username=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change
    """
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(write_only=True)

    def validate_current_password(self, value):
        """Validate current password"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value

    def validate(self, attrs):
        """Validate new password confirmation"""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match.")
        return attrs

    def save(self):
        """Update user password"""
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer for password reset request
    """
    email = serializers.EmailField()

    def validate_email(self, value):
        """Validate that user exists"""
        try:
            user = User.objects.get(email=value.lower())
            self.user = user
            return value.lower()
        except User.DoesNotExist:
            # Don't reveal that user doesn't exist for security
            return value.lower()


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for password reset confirmation
    """
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(write_only=True)

    def validate_token(self, value):
        """Validate reset token"""
        try:
            token = PasswordResetToken.objects.get(token=value)
            if not token.is_valid:
                raise serializers.ValidationError("Token is invalid or expired.")
            self.reset_token = token
            return value
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError("Invalid token.")

    def validate(self, attrs):
        """Validate password confirmation"""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs

    def save(self):
        """Reset user password"""
        user = self.reset_token.user
        user.set_password(self.validated_data['new_password'])
        user.save()
        
        # Mark token as used
        self.reset_token.is_used = True
        self.reset_token.save()
        
        return user


class EmailVerificationSerializer(serializers.Serializer):
    """
    Serializer for email verification
    """
    token = serializers.CharField()

    def validate_token(self, value):
        """Validate verification token"""
        try:
            token = EmailVerificationToken.objects.get(token=value)
            if not token.is_valid:
                raise serializers.ValidationError("Token is invalid or expired.")
            self.verification_token = token
            return value
        except EmailVerificationToken.DoesNotExist:
            raise serializers.ValidationError("Invalid token.")

    def save(self):
        """Verify user email"""
        user = self.verification_token.user
        user.is_email_verified = True
        user.save()
        
        # Mark token as used
        self.verification_token.is_used = True
        self.verification_token.save()
        
        return user


class UserBasicSerializer(serializers.ModelSerializer):
    """
    Basic user serializer for foreign key relationships
    """
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'full_name']