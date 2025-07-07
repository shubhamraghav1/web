from rest_framework import serializers
from .models import DashboardSummary, NotificationSetting, ActivityLog, UserPreference
from policies.serializers import PolicyListSerializer
from family.serializers import FamilyMemberListSerializer


class DashboardSummarySerializer(serializers.ModelSerializer):
    """
    Serializer for dashboard summary statistics
    """
    
    class Meta:
        model = DashboardSummary
        fields = [
            'total_policies', 'active_policies', 'policies_due_soon', 'overdue_policies',
            'total_family_members', 'total_annual_premiums', 'total_coverage_amount',
            'total_documents', 'last_updated'
        ]
        read_only_fields = ['last_updated']


class NotificationSettingSerializer(serializers.ModelSerializer):
    """
    Serializer for notification settings
    """
    notification_type_display = serializers.CharField(source='get_notification_type_display', read_only=True)
    
    class Meta:
        model = NotificationSetting
        fields = [
            'id', 'notification_type', 'notification_type_display', 'is_enabled',
            'premium_due_reminder', 'policy_expiry_reminder', 'document_expiry_reminder',
            'premium_reminder_days', 'policy_expiry_reminder_days', 'document_expiry_reminder_days',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_premium_reminder_days(self, value):
        """Validate premium reminder days"""
        if value < 1 or value > 365:
            raise serializers.ValidationError("Premium reminder days must be between 1 and 365.")
        return value

    def validate_policy_expiry_reminder_days(self, value):
        """Validate policy expiry reminder days"""
        if value < 1 or value > 365:
            raise serializers.ValidationError("Policy expiry reminder days must be between 1 and 365.")
        return value

    def validate_document_expiry_reminder_days(self, value):
        """Validate document expiry reminder days"""
        if value < 1 or value > 365:
            raise serializers.ValidationError("Document expiry reminder days must be between 1 and 365.")
        return value

    def create(self, validated_data):
        """Create notification setting linked to current user"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ActivityLogSerializer(serializers.ModelSerializer):
    """
    Serializer for activity logs
    """
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    object_type_display = serializers.CharField(source='get_object_type_display', read_only=True)
    
    class Meta:
        model = ActivityLog
        fields = [
            'id', 'action', 'action_display', 'object_type', 'object_type_display',
            'object_id', 'object_name', 'description', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class UserPreferenceSerializer(serializers.ModelSerializer):
    """
    Serializer for user preferences
    """
    theme_display = serializers.CharField(source='get_theme_display', read_only=True)
    currency_display = serializers.CharField(source='get_currency_display', read_only=True)
    
    class Meta:
        model = UserPreference
        fields = [
            'id', 'theme', 'theme_display', 'currency', 'currency_display', 'date_format',
            'show_welcome_message', 'default_dashboard_view', 'analytics_enabled',
            'error_reporting_enabled', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_date_format(self, value):
        """Validate date format"""
        allowed_formats = ['MM/DD/YYYY', 'DD/MM/YYYY', 'YYYY-MM-DD', 'MM-DD-YYYY', 'DD-MM-YYYY']
        if value not in allowed_formats:
            raise serializers.ValidationError(f"Date format must be one of: {', '.join(allowed_formats)}")
        return value


class DashboardDataSerializer(serializers.Serializer):
    """
    Comprehensive dashboard data serializer
    """
    summary = DashboardSummarySerializer(read_only=True)
    recent_policies = PolicyListSerializer(many=True, read_only=True)
    due_soon_policies = PolicyListSerializer(many=True, read_only=True)
    overdue_policies = PolicyListSerializer(many=True, read_only=True)
    family_members = FamilyMemberListSerializer(many=True, read_only=True)
    recent_activities = ActivityLogSerializer(many=True, read_only=True)
    notification_settings = NotificationSettingSerializer(many=True, read_only=True)
    user_preferences = UserPreferenceSerializer(read_only=True)


class QuickStatsSerializer(serializers.Serializer):
    """
    Quick statistics for dashboard widgets
    """
    total_policies = serializers.IntegerField()
    active_policies = serializers.IntegerField()
    policies_due_soon = serializers.IntegerField()
    overdue_policies = serializers.IntegerField()
    total_family_members = serializers.IntegerField()
    total_annual_premiums = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_coverage_amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_documents = serializers.IntegerField()
    next_due_date = serializers.DateField(allow_null=True)
    next_due_policy_name = serializers.CharField(allow_null=True)


class UpcomingRemindersSerializer(serializers.Serializer):
    """
    Serializer for upcoming reminders and notifications
    """
    policy_id = serializers.IntegerField()
    policy_name = serializers.CharField()
    policy_type = serializers.CharField()
    insurer_name = serializers.CharField()
    due_date = serializers.DateField()
    days_until_due = serializers.IntegerField()
    premium_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    reminder_type = serializers.CharField()  # 'premium_due', 'policy_expiry', 'document_expiry'


class PolicyTypeStatSerializer(serializers.Serializer):
    """
    Serializer for policy type statistics
    """
    policy_type = serializers.CharField()
    policy_type_display = serializers.CharField()
    count = serializers.IntegerField()
    total_annual_premium = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_coverage = serializers.DecimalField(max_digits=15, decimal_places=2)


class MonthlyPremiumSerializer(serializers.Serializer):
    """
    Serializer for monthly premium breakdown
    """
    month = serializers.CharField()
    total_premium = serializers.DecimalField(max_digits=10, decimal_places=2)
    policy_count = serializers.IntegerField()


class RecentActivitySerializer(serializers.Serializer):
    """
    Serializer for recent user activities
    """
    activity_type = serializers.CharField()
    description = serializers.CharField()
    timestamp = serializers.DateTimeField()
    object_name = serializers.CharField()
    action = serializers.CharField()