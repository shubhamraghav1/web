from rest_framework import serializers
from django.utils import timezone
from decimal import Decimal
from .models import Policy, PolicyDocument, PolicyBeneficiary
from family.serializers import FamilyMemberBasicSerializer


class PolicyDocumentSerializer(serializers.ModelSerializer):
    """
    Serializer for policy documents
    """
    file_extension = serializers.ReadOnlyField()
    is_image = serializers.ReadOnlyField()
    is_pdf = serializers.ReadOnlyField()
    human_readable_size = serializers.ReadOnlyField()
    document_type_display = serializers.CharField(source='get_document_type_display', read_only=True)
    
    class Meta:
        model = PolicyDocument
        fields = [
            'id', 'title', 'document_type', 'document_type_display', 'description',
            'document_file', 'file_size', 'file_type', 'file_extension',
            'is_image', 'is_pdf', 'human_readable_size',
            'document_date', 'expiry_date', 'is_sensitive',
            'uploaded_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'file_size', 'file_type', 'uploaded_at', 'updated_at']

    def validate_document_file(self, value):
        """Validate uploaded file"""
        if value:
            # Check file size (10MB limit)
            if value.size > 10 * 1024 * 1024:
                raise serializers.ValidationError("File size cannot exceed 10MB.")
            
            # Check file type
            allowed_types = [
                'application/pdf',
                'image/jpeg', 'image/jpg', 'image/png', 'image/gif',
                'application/msword',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            ]
            
            if value.content_type not in allowed_types:
                raise serializers.ValidationError(
                    "Unsupported file type. Allowed types: PDF, JPG, PNG, GIF, DOC, DOCX."
                )
        
        return value

    def validate_document_date(self, value):
        """Validate document date is not in the future"""
        if value and value > timezone.now().date():
            raise serializers.ValidationError("Document date cannot be in the future.")
        return value

    def validate_expiry_date(self, value):
        """Validate expiry date"""
        if value:
            document_date = self.initial_data.get('document_date')
            if document_date and value <= document_date:
                raise serializers.ValidationError("Expiry date must be after document date.")
        return value


class PolicyBeneficiarySerializer(serializers.ModelSerializer):
    """
    Serializer for policy beneficiaries
    """
    family_member_details = FamilyMemberBasicSerializer(source='family_member', read_only=True)
    beneficiary_name = serializers.ReadOnlyField()
    relationship = serializers.ReadOnlyField()
    beneficiary_type_display = serializers.CharField(source='get_beneficiary_type_display', read_only=True)
    
    class Meta:
        model = PolicyBeneficiary
        fields = [
            'id', 'family_member', 'family_member_details', 'external_name',
            'external_relationship', 'external_contact_info', 'beneficiary_name',
            'relationship', 'beneficiary_type', 'beneficiary_type_display',
            'percentage', 'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_percentage(self, value):
        """Validate percentage is between 0 and 100"""
        if value < 0 or value > 100:
            raise serializers.ValidationError("Percentage must be between 0 and 100.")
        return value

    def validate(self, attrs):
        """Validate beneficiary data"""
        family_member = attrs.get('family_member')
        external_name = attrs.get('external_name')
        
        # Must have either family member or external name
        if not family_member and not external_name:
            raise serializers.ValidationError(
                "Must specify either a family member or external beneficiary name."
            )
        
        # Cannot have both family member and external data
        if family_member and external_name:
            raise serializers.ValidationError(
                "Cannot specify both family member and external beneficiary data."
            )
        
        # If external beneficiary, external_relationship is required
        if external_name and not attrs.get('external_relationship'):
            raise serializers.ValidationError(
                "External relationship is required for external beneficiaries."
            )
        
        return attrs


class PolicySerializer(serializers.ModelSerializer):
    """
    Full serializer for policy management
    """
    policyholder_details = FamilyMemberBasicSerializer(source='policyholder', read_only=True)
    documents = PolicyDocumentSerializer(many=True, read_only=True)
    beneficiaries = PolicyBeneficiarySerializer(many=True, read_only=True)
    
    # Computed fields
    days_until_due = serializers.ReadOnlyField()
    is_due_soon = serializers.ReadOnlyField()
    is_overdue = serializers.ReadOnlyField()
    annual_premium = serializers.ReadOnlyField()
    coverage_summary = serializers.ReadOnlyField()
    
    # Display fields
    policy_type_display = serializers.CharField(source='get_policy_type_display', read_only=True)
    premium_frequency_display = serializers.CharField(source='get_premium_frequency_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Policy
        fields = [
            'id', 'policyholder', 'policyholder_details', 'policy_number', 'policy_type',
            'policy_type_display', 'insurer_name', 'insurer_contact_info', 'policy_name',
            'description', 'coverage_amount', 'deductible', 'premium_amount',
            'premium_frequency', 'premium_frequency_display', 'policy_start_date',
            'policy_end_date', 'premium_due_date', 'last_premium_paid_date',
            'status', 'status_display', 'agent_name', 'agent_contact_info', 'notes',
            'notification_days_before', 'is_auto_renew', 'days_until_due',
            'is_due_soon', 'is_overdue', 'annual_premium', 'coverage_summary',
            'documents', 'beneficiaries', 'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_policy_start_date(self, value):
        """Validate policy start date"""
        if value and value > timezone.now().date():
            # Allow future start dates but warn if too far in future
            if (value - timezone.now().date()).days > 365:
                raise serializers.ValidationError(
                    "Policy start date cannot be more than 1 year in the future."
                )
        return value

    def validate_policy_end_date(self, value):
        """Validate policy end date"""
        if value:
            start_date = self.initial_data.get('policy_start_date')
            if start_date and value <= start_date:
                raise serializers.ValidationError("Policy end date must be after start date.")
        return value

    def validate_premium_due_date(self, value):
        """Validate premium due date"""
        if value:
            start_date = self.initial_data.get('policy_start_date')
            if start_date and value < start_date:
                raise serializers.ValidationError("Premium due date cannot be before policy start date.")
        return value

    def validate_coverage_amount(self, value):
        """Validate coverage amount"""
        if value is not None and value <= 0:
            raise serializers.ValidationError("Coverage amount must be positive.")
        return value

    def validate_premium_amount(self, value):
        """Validate premium amount"""
        if value <= 0:
            raise serializers.ValidationError("Premium amount must be positive.")
        return value

    def validate_deductible(self, value):
        """Validate deductible"""
        if value is not None and value < 0:
            raise serializers.ValidationError("Deductible cannot be negative.")
        return value

    def validate_notification_days_before(self, value):
        """Validate notification days"""
        if value < 0 or value > 365:
            raise serializers.ValidationError("Notification days must be between 0 and 365.")
        return value

    def validate(self, attrs):
        """Custom validation for policy"""
        # Validate that policyholder belongs to current user
        user = self.context['request'].user
        policyholder = attrs.get('policyholder')
        
        if policyholder and policyholder.user != user:
            raise serializers.ValidationError("Policyholder must be one of your family members.")
        
        # Check for duplicate policy numbers for the same insurer and user
        policy_number = attrs.get('policy_number')
        insurer_name = attrs.get('insurer_name')
        
        if policy_number and insurer_name:
            query = Policy.objects.filter(
                user=user,
                policy_number=policy_number,
                insurer_name=insurer_name
            )
            
            # Exclude current instance if updating
            if self.instance:
                query = query.exclude(pk=self.instance.pk)
            
            if query.exists():
                raise serializers.ValidationError(
                    "A policy with this number already exists for this insurer."
                )
        
        return attrs

    def create(self, validated_data):
        """Create policy linked to current user"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class PolicyListSerializer(serializers.ModelSerializer):
    """
    Serializer for policy list view (minimal fields)
    """
    policyholder_name = serializers.CharField(source='policyholder.full_name', read_only=True)
    policy_type_display = serializers.CharField(source='get_policy_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    days_until_due = serializers.ReadOnlyField()
    is_due_soon = serializers.ReadOnlyField()
    is_overdue = serializers.ReadOnlyField()
    annual_premium = serializers.ReadOnlyField()
    document_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Policy
        fields = [
            'id', 'policy_name', 'policy_number', 'policy_type', 'policy_type_display',
            'insurer_name', 'policyholder_name', 'premium_amount', 'premium_frequency',
            'premium_due_date', 'status', 'status_display', 'days_until_due',
            'is_due_soon', 'is_overdue', 'annual_premium', 'document_count', 'is_active'
        ]
    
    def get_document_count(self, obj):
        """Get count of documents for this policy"""
        return obj.documents.filter(is_active=True).count()


class PolicyCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating policies with required fields only
    """
    
    class Meta:
        model = Policy
        fields = [
            'policyholder', 'policy_number', 'policy_type', 'insurer_name',
            'policy_name', 'premium_amount', 'premium_frequency',
            'policy_start_date', 'premium_due_date', 'coverage_amount'
        ]

    def validate(self, attrs):
        """Validate policy creation"""
        # Validate that policyholder belongs to current user
        user = self.context['request'].user
        policyholder = attrs.get('policyholder')
        
        if policyholder and policyholder.user != user:
            raise serializers.ValidationError("Policyholder must be one of your family members.")
        
        return attrs

    def create(self, validated_data):
        """Create policy linked to current user"""
        validated_data['user'] = self.context['request'].user
        return Policy.objects.create(**validated_data)


class PolicyUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating policies (excludes certain fields)
    """
    days_until_due = serializers.ReadOnlyField()
    annual_premium = serializers.ReadOnlyField()
    
    class Meta:
        model = Policy
        fields = [
            'policy_name', 'description', 'coverage_amount', 'deductible',
            'premium_amount', 'premium_frequency', 'policy_end_date',
            'premium_due_date', 'last_premium_paid_date', 'status',
            'agent_name', 'agent_contact_info', 'notes',
            'notification_days_before', 'is_auto_renew', 'is_active'
        ]

    def validate_premium_amount(self, value):
        """Validate premium amount"""
        if value <= 0:
            raise serializers.ValidationError("Premium amount must be positive.")
        return value


class PolicyBasicSerializer(serializers.ModelSerializer):
    """
    Basic policy serializer for foreign key relationships
    """
    policy_type_display = serializers.CharField(source='get_policy_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Policy
        fields = [
            'id', 'policy_name', 'policy_number', 'policy_type',
            'policy_type_display', 'insurer_name', 'status', 'status_display'
        ]