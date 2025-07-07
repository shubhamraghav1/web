from django.db import models
from django.conf import settings
from django.utils import timezone


class DashboardSummary(models.Model):
    """
    Model to cache dashboard summary data for performance
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='dashboard_summary'
    )
    
    # Policy statistics
    total_policies = models.PositiveIntegerField(default=0)
    active_policies = models.PositiveIntegerField(default=0)
    policies_due_soon = models.PositiveIntegerField(default=0)
    overdue_policies = models.PositiveIntegerField(default=0)
    
    # Family statistics
    total_family_members = models.PositiveIntegerField(default=0)
    
    # Financial statistics
    total_annual_premiums = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_coverage_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Document statistics
    total_documents = models.PositiveIntegerField(default=0)
    
    # Timestamps
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'dashboard_summaries'
        verbose_name = 'Dashboard Summary'
        verbose_name_plural = 'Dashboard Summaries'
    
    def __str__(self):
        return f"Dashboard Summary for {self.user.email}"
    
    def update_summary(self):
        """Update summary statistics"""
        from policies.models import Policy
        from family.models import FamilyMember
        
        # Policy statistics
        user_policies = Policy.objects.filter(user=self.user, is_active=True)
        self.total_policies = user_policies.count()
        self.active_policies = user_policies.filter(status='active').count()
        self.policies_due_soon = user_policies.filter(is_due_soon=True).count()
        self.overdue_policies = user_policies.filter(is_overdue=True).count()
        
        # Family statistics
        self.total_family_members = FamilyMember.objects.filter(
            user=self.user, is_active=True
        ).count()
        
        # Financial statistics
        self.total_annual_premiums = sum(
            policy.annual_premium for policy in user_policies
        )
        self.total_coverage_amount = sum(
            policy.coverage_amount or 0 for policy in user_policies
        )
        
        # Document statistics
        self.total_documents = sum(
            policy.documents.filter(is_active=True).count() 
            for policy in user_policies
        )
        
        self.save()


class NotificationSetting(models.Model):
    """
    Model for user notification preferences
    """
    NOTIFICATION_TYPE_CHOICES = [
        ('email', 'Email'),
        ('push', 'Push Notification'),
        ('sms', 'SMS'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notification_settings'
    )
    
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    is_enabled = models.BooleanField(default=True)
    
    # Notification timing
    premium_due_reminder = models.BooleanField(default=True)
    policy_expiry_reminder = models.BooleanField(default=True)
    document_expiry_reminder = models.BooleanField(default=True)
    
    # Timing preferences (days before)
    premium_reminder_days = models.PositiveIntegerField(default=30)
    policy_expiry_reminder_days = models.PositiveIntegerField(default=60)
    document_expiry_reminder_days = models.PositiveIntegerField(default=30)
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'notification_settings'
        verbose_name = 'Notification Setting'
        verbose_name_plural = 'Notification Settings'
        unique_together = ['user', 'notification_type']
    
    def __str__(self):
        return f"{self.user.email} - {self.get_notification_type_display()}"


class ActivityLog(models.Model):
    """
    Model to track user activities for dashboard display
    """
    ACTION_CHOICES = [
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('deleted', 'Deleted'),
        ('uploaded', 'Uploaded'),
        ('viewed', 'Viewed'),
    ]
    
    OBJECT_TYPE_CHOICES = [
        ('policy', 'Policy'),
        ('family_member', 'Family Member'),
        ('document', 'Document'),
        ('beneficiary', 'Beneficiary'),
        ('profile', 'Profile'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='activity_logs'
    )
    
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    object_type = models.CharField(max_length=20, choices=OBJECT_TYPE_CHOICES)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    object_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Metadata
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    # Timestamp
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'activity_logs'
        verbose_name = 'Activity Log'
        verbose_name_plural = 'Activity Logs'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} {self.action} {self.object_type}: {self.object_name}"


class UserPreference(models.Model):
    """
    Model for storing user preferences and settings
    """
    THEME_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('auto', 'Auto'),
    ]
    
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
        ('CAD', 'Canadian Dollar'),
    ]
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='preferences'
    )
    
    # UI Preferences
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='light')
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    date_format = models.CharField(max_length=20, default='MM/DD/YYYY')
    
    # Dashboard preferences
    show_welcome_message = models.BooleanField(default=True)
    default_dashboard_view = models.CharField(
        max_length=20, 
        choices=[
            ('summary', 'Summary'),
            ('policies', 'Policies'),
            ('calendar', 'Calendar'),
        ],
        default='summary'
    )
    
    # Privacy preferences
    analytics_enabled = models.BooleanField(default=True)
    error_reporting_enabled = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_preferences'
        verbose_name = 'User Preference'
        verbose_name_plural = 'User Preferences'
    
    def __str__(self):
        return f"Preferences for {self.user.email}"
