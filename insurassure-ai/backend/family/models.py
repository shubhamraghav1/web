from django.db import models
from django.conf import settings
from django.utils import timezone


class FamilyMember(models.Model):
    """
    Model to represent family members for insurance management
    """
    
    RELATIONSHIP_CHOICES = [
        ('self', 'Self'),
        ('spouse', 'Spouse'),
        ('child', 'Child'),
        ('parent', 'Parent'),
        ('sibling', 'Sibling'),
        ('grandparent', 'Grandparent'),
        ('grandchild', 'Grandchild'),
        ('other', 'Other'),
    ]
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('N', 'Prefer not to say'),
    ]
    
    # Linked to the user who created this family member
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='family_members'
    )
    
    # Basic information
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    
    # Relationship to the primary user
    relationship = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES)
    
    # Contact information
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    
    # Address information
    address_line_1 = models.CharField(max_length=100, blank=True)
    address_line_2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=50, blank=True, default='US')
    
    # Additional information
    ssn_last_four = models.CharField(max_length=4, blank=True, help_text="Last 4 digits of SSN")
    notes = models.TextField(blank=True)
    
    # Photo
    photo = models.ImageField(upload_to='family_photos/', blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'family_members'
        verbose_name = 'Family Member'
        verbose_name_plural = 'Family Members'
        unique_together = ['user', 'first_name', 'last_name', 'date_of_birth']
        ordering = ['relationship', 'first_name', 'last_name']
    
    def __str__(self):
        return f"{self.full_name} ({self.get_relationship_display()})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def age(self):
        """Calculate age based on date of birth"""
        if not self.date_of_birth:
            return None
        
        today = timezone.now().date()
        age = today.year - self.date_of_birth.year
        
        # Adjust if birthday hasn't occurred this year
        if today.month < self.date_of_birth.month or \
           (today.month == self.date_of_birth.month and today.day < self.date_of_birth.day):
            age -= 1
        
        return age
    
    @property
    def full_address(self):
        """Get formatted full address"""
        address_parts = []
        
        if self.address_line_1:
            address_parts.append(self.address_line_1)
        if self.address_line_2:
            address_parts.append(self.address_line_2)
        
        city_state_zip = []
        if self.city:
            city_state_zip.append(self.city)
        if self.state:
            city_state_zip.append(self.state)
        if self.zip_code:
            city_state_zip.append(self.zip_code)
        
        if city_state_zip:
            address_parts.append(', '.join(city_state_zip))
        
        if self.country and self.country != 'US':
            address_parts.append(self.country)
        
        return '\n'.join(address_parts) if address_parts else ''
    
    def save(self, *args, **kwargs):
        if self.pk:  # Update
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)
