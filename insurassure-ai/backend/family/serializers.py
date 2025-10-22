from rest_framework import serializers
from django.utils import timezone
from .models import FamilyMember


class FamilyMemberSerializer(serializers.ModelSerializer):
    """
    Serializer for family member management
    """
    full_name = serializers.ReadOnlyField()
    age = serializers.ReadOnlyField()
    full_address = serializers.ReadOnlyField()
    relationship_display = serializers.CharField(source='get_relationship_display', read_only=True)
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    
    class Meta:
        model = FamilyMember
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'date_of_birth', 'age',
            'gender', 'gender_display', 'relationship', 'relationship_display',
            'email', 'phone_number', 'address_line_1', 'address_line_2',
            'city', 'state', 'zip_code', 'country', 'full_address',
            'ssn_last_four', 'notes', 'photo', 'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_date_of_birth(self, value):
        """Validate date of birth is not in the future"""
        if value > timezone.now().date():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return value

    def validate_ssn_last_four(self, value):
        """Validate SSN last four digits"""
        if value and (not value.isdigit() or len(value) != 4):
            raise serializers.ValidationError("SSN last four must be exactly 4 digits.")
        return value

    def validate_zip_code(self, value):
        """Basic ZIP code validation"""
        if value and not (value.replace('-', '').isdigit() and len(value.replace('-', '')) in [5, 9]):
            raise serializers.ValidationError("Invalid ZIP code format.")
        return value

    def validate(self, attrs):
        """Custom validation for family member"""
        # Check for duplicate family members (same name and DOB for the same user)
        user = self.context['request'].user
        first_name = attrs.get('first_name')
        last_name = attrs.get('last_name')
        date_of_birth = attrs.get('date_of_birth')
        
        if first_name and last_name and date_of_birth:
            query = FamilyMember.objects.filter(
                user=user,
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth
            )
            
            # Exclude current instance if updating
            if self.instance:
                query = query.exclude(pk=self.instance.pk)
            
            if query.exists():
                raise serializers.ValidationError(
                    "A family member with the same name and date of birth already exists."
                )
        
        return attrs

    def create(self, validated_data):
        """Create family member linked to current user"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class FamilyMemberBasicSerializer(serializers.ModelSerializer):
    """
    Basic family member serializer for foreign key relationships
    """
    full_name = serializers.ReadOnlyField()
    age = serializers.ReadOnlyField()
    relationship_display = serializers.CharField(source='get_relationship_display', read_only=True)
    
    class Meta:
        model = FamilyMember
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'age',
            'relationship', 'relationship_display', 'date_of_birth'
        ]


class FamilyMemberListSerializer(serializers.ModelSerializer):
    """
    Serializer for family member list view (minimal fields)
    """
    full_name = serializers.ReadOnlyField()
    age = serializers.ReadOnlyField()
    relationship_display = serializers.CharField(source='get_relationship_display', read_only=True)
    policy_count = serializers.SerializerMethodField()
    
    class Meta:
        model = FamilyMember
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'age',
            'relationship', 'relationship_display', 'photo', 'policy_count', 'is_active'
        ]
    
    def get_policy_count(self, obj):
        """Get count of policies for this family member"""
        return obj.policies_as_holder.filter(is_active=True).count()


class FamilyMemberCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating family members with minimal required fields
    """
    
    class Meta:
        model = FamilyMember
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'relationship', 'gender',
            'email', 'phone_number'
        ]

    def validate_date_of_birth(self, value):
        """Validate date of birth is not in the future"""
        if value > timezone.now().date():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return value

    def create(self, validated_data):
        """Create family member linked to current user"""
        validated_data['user'] = self.context['request'].user
        return FamilyMember.objects.create(**validated_data)


class FamilyMemberUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating family members (excludes certain fields)
    """
    full_name = serializers.ReadOnlyField()
    age = serializers.ReadOnlyField()
    
    class Meta:
        model = FamilyMember
        fields = [
            'first_name', 'last_name', 'full_name', 'date_of_birth', 'age',
            'gender', 'relationship', 'email', 'phone_number',
            'address_line_1', 'address_line_2', 'city', 'state', 'zip_code', 'country',
            'ssn_last_four', 'notes', 'photo', 'is_active'
        ]

    def validate_date_of_birth(self, value):
        """Validate date of birth is not in the future"""
        if value > timezone.now().date():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return value

    def validate_ssn_last_four(self, value):
        """Validate SSN last four digits"""
        if value and (not value.isdigit() or len(value) != 4):
            raise serializers.ValidationError("SSN last four must be exactly 4 digits.")
        return value