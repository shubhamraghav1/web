from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal
import os
import uuid


def policy_document_upload_path(instance, filename):
    """
    Generate upload path for policy documents
    """
    # Get file extension
    ext = filename.split('.')[-1].lower()
    # Generate new filename with UUID
    new_filename = f"{uuid.uuid4()}.{ext}"
    # Return path: policy_documents/user_id/policy_id/filename
    return f"policy_documents/{instance.policy.user.id}/{instance.policy.id}/{new_filename}"


class Policy(models.Model):
    """
    Model to represent insurance policies
    """
    
    POLICY_TYPE_CHOICES = [
        ('auto', 'Auto Insurance'),
        ('home', 'Home Insurance'),
        ('life', 'Life Insurance'),
        ('health', 'Health Insurance'),
        ('dental', 'Dental Insurance'),
        ('vision', 'Vision Insurance'),
        ('disability', 'Disability Insurance'),
        ('travel', 'Travel Insurance'),
        ('pet', 'Pet Insurance'),
        ('umbrella', 'Umbrella Insurance'),
        ('renters', 'Renters Insurance'),
        ('business', 'Business Insurance'),
        ('other', 'Other'),
    ]
    
    PREMIUM_FREQUENCY_CHOICES = [
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('semi_annually', 'Semi-Annually'),
        ('annually', 'Annually'),
        ('one_time', 'One Time'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
        ('pending', 'Pending'),
        ('suspended', 'Suspended'),
    ]
    
    # Linked to the user who owns this policy
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='policies'
    )
    
    # Linked to the family member this policy covers (if applicable)
    policyholder = models.ForeignKey(
        'family.FamilyMember',
        on_delete=models.CASCADE,
        related_name='policies_as_holder',
        help_text="The family member who is the primary policyholder"
    )
    
    # Basic policy information
    policy_number = models.CharField(max_length=100)
    policy_type = models.CharField(max_length=20, choices=POLICY_TYPE_CHOICES)
    insurer_name = models.CharField(max_length=100)
    insurer_contact_info = models.TextField(blank=True, help_text="Phone, email, address, etc.")
    
    # Policy details
    policy_name = models.CharField(max_length=200, help_text="Custom name for easy identification")
    description = models.TextField(blank=True)
    
    # Coverage details
    coverage_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Total coverage amount"
    )
    deductible = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    
    # Premium information
    premium_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Premium amount per frequency period"
    )
    premium_frequency = models.CharField(max_length=20, choices=PREMIUM_FREQUENCY_CHOICES)
    
    # Important dates
    policy_start_date = models.DateField()
    policy_end_date = models.DateField(null=True, blank=True)
    premium_due_date = models.DateField(help_text="Next premium due date")
    last_premium_paid_date = models.DateField(null=True, blank=True)
    
    # Policy status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Additional information
    agent_name = models.CharField(max_length=100, blank=True)
    agent_contact_info = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    # Notification settings
    notification_days_before = models.PositiveIntegerField(
        default=30,
        help_text="Days before premium due date to send notification"
    )
    is_auto_renew = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'policies'
        verbose_name = 'Policy'
        verbose_name_plural = 'Policies'
        ordering = ['-premium_due_date', 'policy_type', 'insurer_name']
        unique_together = ['user', 'policy_number', 'insurer_name']
    
    def __str__(self):
        return f"{self.policy_name} - {self.insurer_name} ({self.policy_number})"
    
    @property
    def days_until_due(self):
        """Calculate days until premium due date"""
        if not self.premium_due_date:
            return None
        
        today = timezone.now().date()
        delta = self.premium_due_date - today
        return delta.days
    
    @property
    def is_due_soon(self):
        """Check if premium is due within notification period"""
        days_until = self.days_until_due
        if days_until is None:
            return False
        return 0 <= days_until <= self.notification_days_before
    
    @property
    def is_overdue(self):
        """Check if premium payment is overdue"""
        days_until = self.days_until_due
        if days_until is None:
            return False
        return days_until < 0
    
    @property
    def annual_premium(self):
        """Calculate annual premium amount"""
        if not self.premium_amount:
            return Decimal('0.00')
        
        frequency_multiplier = {
            'monthly': 12,
            'quarterly': 4,
            'semi_annually': 2,
            'annually': 1,
            'one_time': 1,
        }
        
        multiplier = frequency_multiplier.get(self.premium_frequency, 1)
        return self.premium_amount * multiplier
    
    @property
    def coverage_summary(self):
        """Get a summary of coverage details"""
        summary = []
        if self.coverage_amount:
            summary.append(f"Coverage: ${self.coverage_amount:,.2f}")
        if self.deductible:
            summary.append(f"Deductible: ${self.deductible:,.2f}")
        return " | ".join(summary) if summary else "No coverage details"
    
    def get_next_due_date(self):
        """Calculate next premium due date based on frequency"""
        if not self.premium_due_date:
            return None
        
        from dateutil.relativedelta import relativedelta
        
        frequency_delta = {
            'monthly': relativedelta(months=1),
            'quarterly': relativedelta(months=3),
            'semi_annually': relativedelta(months=6),
            'annually': relativedelta(years=1),
            'one_time': None,
        }
        
        delta = frequency_delta.get(self.premium_frequency)
        if delta:
            return self.premium_due_date + delta
        return None
    
    def update_premium_due_date(self):
        """Update premium due date to next occurrence"""
        next_date = self.get_next_due_date()
        if next_date:
            self.premium_due_date = next_date
            self.save(update_fields=['premium_due_date', 'updated_at'])
    
    def save(self, *args, **kwargs):
        if self.pk:  # Update
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)


class PolicyDocument(models.Model):
    """
    Model to store documents related to insurance policies
    """
    
    DOCUMENT_TYPE_CHOICES = [
        ('policy', 'Policy Document'),
        ('certificate', 'Certificate of Insurance'),
        ('receipt', 'Premium Payment Receipt'),
        ('claim', 'Claim Document'),
        ('correspondence', 'Correspondence'),
        ('id_card', 'Insurance ID Card'),
        ('declaration', 'Declaration Page'),
        ('amendment', 'Policy Amendment'),
        ('other', 'Other'),
    ]
    
    # Linked to the policy
    policy = models.ForeignKey(
        Policy,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    
    # Document information
    title = models.CharField(max_length=200)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES)
    description = models.TextField(blank=True)
    
    # File upload
    document_file = models.FileField(
        upload_to=policy_document_upload_path,
        help_text="Supported formats: PDF, JPG, PNG, DOC, DOCX"
    )
    file_size = models.PositiveIntegerField(null=True, blank=True, help_text="File size in bytes")
    file_type = models.CharField(max_length=50, blank=True)
    
    # Document metadata
    document_date = models.DateField(
        null=True, 
        blank=True,
        help_text="Date the document was created/issued"
    )
    expiry_date = models.DateField(
        null=True, 
        blank=True,
        help_text="When this document expires (if applicable)"
    )
    
    # Access and security
    is_sensitive = models.BooleanField(
        default=False,
        help_text="Mark as sensitive for additional security"
    )
    
    # Timestamps
    uploaded_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'policy_documents'
        verbose_name = 'Policy Document'
        verbose_name_plural = 'Policy Documents'
        ordering = ['-uploaded_at', 'document_type', 'title']
    
    def __str__(self):
        return f"{self.title} ({self.policy.policy_name})"
    
    @property
    def file_extension(self):
        """Get file extension"""
        if self.document_file and self.document_file.name:
            return os.path.splitext(self.document_file.name)[1].lower()
        return ''
    
    @property
    def is_image(self):
        """Check if document is an image"""
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        return self.file_extension in image_extensions
    
    @property
    def is_pdf(self):
        """Check if document is a PDF"""
        return self.file_extension == '.pdf'
    
    @property
    def human_readable_size(self):
        """Get human readable file size"""
        if not self.file_size:
            return "Unknown size"
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if self.file_size < 1024.0:
                return f"{self.file_size:.1f} {unit}"
            self.file_size /= 1024.0
        return f"{self.file_size:.1f} TB"
    
    def save(self, *args, **kwargs):
        # Set file size and type if not already set
        if self.document_file and not self.file_size:
            self.file_size = self.document_file.size
        
        if self.document_file and not self.file_type:
            self.file_type = self.document_file.content_type or 'application/octet-stream'
        
        if self.pk:  # Update
            self.updated_at = timezone.now()
            
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Delete the file from storage when the model is deleted
        if self.document_file:
            self.document_file.delete(save=False)
        super().delete(*args, **kwargs)


class PolicyBeneficiary(models.Model):
    """
    Model to track beneficiaries for life insurance and other applicable policies
    """
    
    BENEFICIARY_TYPE_CHOICES = [
        ('primary', 'Primary Beneficiary'),
        ('contingent', 'Contingent Beneficiary'),
        ('revocable', 'Revocable Beneficiary'),
        ('irrevocable', 'Irrevocable Beneficiary'),
    ]
    
    policy = models.ForeignKey(
        Policy,
        on_delete=models.CASCADE,
        related_name='beneficiaries'
    )
    
    # Beneficiary can be a family member or external person
    family_member = models.ForeignKey(
        'family.FamilyMember',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='beneficiary_policies'
    )
    
    # For external beneficiaries (not family members)
    external_name = models.CharField(max_length=100, blank=True)
    external_relationship = models.CharField(max_length=50, blank=True)
    external_contact_info = models.TextField(blank=True)
    
    # Beneficiary details
    beneficiary_type = models.CharField(max_length=20, choices=BENEFICIARY_TYPE_CHOICES)
    percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        default=Decimal('100.00'),
        help_text="Percentage of benefit (e.g., 50.00 for 50%)"
    )
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'policy_beneficiaries'
        verbose_name = 'Policy Beneficiary'
        verbose_name_plural = 'Policy Beneficiaries'
        ordering = ['beneficiary_type', '-percentage']
    
    def __str__(self):
        name = self.family_member.full_name if self.family_member else self.external_name
        return f"{name} - {self.get_beneficiary_type_display()} ({self.percentage}%)"
    
    @property
    def beneficiary_name(self):
        """Get beneficiary name whether family member or external"""
        return self.family_member.full_name if self.family_member else self.external_name
    
    @property
    def relationship(self):
        """Get relationship whether family member or external"""
        if self.family_member:
            return self.family_member.get_relationship_display()
        return self.external_relationship
    
    def save(self, *args, **kwargs):
        if self.pk:  # Update
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)
