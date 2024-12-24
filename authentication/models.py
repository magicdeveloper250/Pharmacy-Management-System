from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from django.contrib.auth.models import AbstractBaseUser, Permission
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
import pytz
import json


class Pharmacy(models.Model):
    pharmacy_name = models.CharField(max_length=100)
    address = models.TextField(null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)
    contact_phone = models.CharField(max_length=15, null=True, blank=True)
    registration_number = models.CharField(max_length=100, null=True, blank=True)
    license_number = models.CharField(max_length=100, null=True, blank=True)
    opening_hours = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.pharmacy_name
    def to_json(self):
        return {
            'id': self.id,
            'pharmacy_name': self.pharmacy_name,
            'address': self.address,
            'contact_email': self.contact_email,
            'contact_phone': self.contact_phone,
            'registration_number': self.registration_number,
            'license_number': self.license_number,
            'opening_hours': self.opening_hours
        }
    
class PharmacyUserManager(BaseUserManager):
    def create_user(self, email, username, pharmacy,phone_number, password=None, profile_picture=None):
        if not email:
            raise ValueError("Pharmacy user must have an email address")
        if not username:
            raise ValueError("Pharmacy user must have a username")
        if not pharmacy:
            raise ValueError("Pharmacy user must be associated with a pharmacy")

        email = self.normalize_email(email)
        user = self.model(
           email=email,
            username=username,
            pharmacy=pharmacy,
            password=password, 
            phone_number=phone_number,
            profile_picture=profile_picture
        )

        user.set_password(password)
        user.is_staff = True
        user.save(using=self._db)
        user.assign_default_permissions()
        return user

    def create_superuser(self, email, username, pharmacy,phone_number, password=None, profile_picture=None):
        user = self.create_user(
            email=email,
            username=username,
            pharmacy=pharmacy,
            password=password, 
            phone_number=phone_number,
            profile_picture=profile_picture
        )
        user.is_admin = True
        user.is_superadmin = True
        user.is_verified = True
        user.save(using=self._db)
        user.assign_default_permissions()
        return user


class PharmacyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    pharmacy = models.ForeignKey(Pharmacy, related_name="users", on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True, null=True)
    profile_picture = models.FileField(upload_to="pharmacy_users/", null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "pharmacy"]

    objects = PharmacyUserManager()

    class Meta:
        permissions = [
            ("view_sales", "Can view pharmacy sales"),
            ("manage_sales", "Can manage pharmacy sales"),
            ("view_purchases", "Can view pharmacy purchases"),
            ("manage_purchases", "Can manage pharmacy purchases"),
            ("view_prescriptions", "Can view prescriptions"),
            ("manage_prescriptions", "Can manage prescriptions"),
            ("manage_users", "Can manage pharmacy staff"),
            ("view_customers", "Can view pharmacy customers"),
            ("manage_customers", "Can manage pharmacy customers"),
            ("view_reports", "Can view pharmacy reports"),
             ("view_suppliers", "Can view pharmacy suppliers"),
            ("manage_supplers", "Can manage pharmacy suplliers"),
            ("view_medicines", "Can view pharmacy medicines"),
            ("manage_medicines", "Can manage pharmacy medicines"),
            ("view_pharmacy_settings", "Can view pharmacy settings"),
            ("manage_pharmacy_settings", "Can manage pharmacy settings"),
        ]

    def __str__(self):
        return f"{self.username} ({self.pharmacy.pharmacy_name})"

    def has_perm(self, perm, obj=None):
        if self.is_superadmin:
            return True
            
        if self.is_admin:
            if obj is None or hasattr(obj, 'pharmacy') and obj.pharmacy == self.pharmacy:
                return True
        if obj is None:
            return super().has_perm(perm)
        if hasattr(obj, 'pharmacy') and obj.pharmacy != self.pharmacy:
            return False
            
        return super().has_perm(perm)

    def has_module_perms(self, app_label):
        if self.is_superadmin:
            return True
            
        if self.is_admin and app_label in ['authentication', 'useradmin']:
            return True
            
        return any(self.has_perm(f"{app_label}.{perm}") 
                  for perm in self.get_all_permissions())

    @property
    def role(self):
        if self.is_superadmin:
            return "Super Admin"
        elif self.is_admin:
            return "Pharmacy Admin"
        elif self.is_staff:
            return "Staff"
        return "Regular User"

    def assign_default_permissions(self):
        if self.is_admin:
            admin_perms = Permission.objects.filter(
                codename__in=[
                    'view_sales', 'manage_sales',
                    'view_purchases', 'manage_purchases',
                    'view_prescriptions', 'manage_prescriptions',
                    'view_customers', 'manage_customers',
                    'view_reports', 'manage_reports',
                ]
            )
            self.user_permissions.set(admin_perms)
            
        elif self.is_staff:

            staff_perms = Permission.objects.filter(
                codename__in=[
                    'view_customers',
                    'view_purchases',
                    'view_prescriptions',
                    'view_reports',
                    'manage_sales',
                ]
            )
            self.user_permissions.set(staff_perms)



class PasswordResetToken(models.Model):
    user= models.ForeignKey(PharmacyUser, on_delete=models.CASCADE, null=False)
    token= models.TextField(  null=False)
    is_active= models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def token_expired(self)->bool:
        expiration_time= self.date_created + timedelta(minutes=settings.RESET_TOKEN_TIMEOUT)
        return timezone.now()>expiration_time
    
    def __str__(self) -> str:
        return str(self.token)
    





class PharmacySettings(models.Model):
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('es', 'Spanish'),
        ('fr', 'French'),
        ('de', 'German'),
        ('ar', 'Arabic'),
    ]

    CURRENCY_CHOICES = [
        ('USD', '$'),
        ('EUR', '€'),
        ('GBP', '£'),
        ('INR', '₹'),
        ('CNY', '¥'),
    ]
    

 
    pharmacy = models.OneToOneField(
        'Pharmacy',
        on_delete=models.CASCADE,
        related_name='settings'
    )
    business_name = models.CharField(max_length=255)
    legal_entity_name = models.CharField(max_length=255, blank=True)
    tax_identification_number = models.CharField(max_length=50, blank=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    address = models.TextField()
    
 
    business_hours = models.JSONField(
        default=dict,
        help_text='Format: {"monday": {"open": "09:00", "close": "18:00"}, ...}'
    )
    
   
    enable_notifications = models.BooleanField(default=True)
    notification_email = models.EmailField(
        blank=True,
        help_text='Email for receiving system notifications'
    )
    low_stock_threshold = models.IntegerField(
        default=10,
        validators=[MinValueValidator(1)]
    )
    enable_low_stock_alerts = models.BooleanField(default=True)
    enable_expiry_alerts = models.BooleanField(default=True)
    expiry_alert_days = models.IntegerField(default=30)
   
    require_prescription_approval = models.BooleanField(default=True)
    allow_digital_prescriptions = models.BooleanField(default=True)
    prescription_validity_days = models.IntegerField(
        default=30,
        validators=[MinValueValidator(1)]
    )
    
     
    auto_order_enabled = models.BooleanField(default=False)
    default_tax_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    allow_partial_fulfillment = models.BooleanField(default=True)
    enable_batch_tracking = models.BooleanField(default=True)
    
  
    receipt_prefix = models.CharField(max_length=10, default='RX')
    receipt_footer_text = models.TextField(blank=True)
    show_tax_on_receipt = models.BooleanField(default=True)
    print_duplicate_receipt = models.BooleanField(default=True)
    
  
    smtp_settings = models.JSONField(
        default=dict,
        help_text='SMTP server configuration for email notifications'
    )
    
    
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='USD'
    )
    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default='en'
    )
    timezone = models.CharField(
        max_length=50,
        default='UTC',
        choices=[(tz, tz) for tz in pytz.all_timezones]
    )
    
   
    enable_audit_trail = models.BooleanField(default=True)
    backup_frequency = models.IntegerField(
        default=7,
        help_text='Backup frequency in days'
    )
    
  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Settings'
        verbose_name_plural = 'Settings'
        permissions = [
            ("manage_settings", "Can manage pharmacy settings"),
            ("view_settings", "Can view pharmacy settings"),
        ]

    def __str__(self):
        return f"Settings for {self.pharmacy.pharmacy_name}"

    def clean(self):
        
        try:
            if self.business_hours:
                hours = json.loads(self.business_hours) if isinstance(self.business_hours, str) else self.business_hours
                days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
                for day in hours:
                    if day.lower() not in days:
                        raise ValidationError(f'Invalid day in business hours: {day}')
                    if 'open' not in hours[day] or 'close' not in hours[day]:
                        raise ValidationError(f'Missing open/close time for {day}')
        except json.JSONDecodeError:
            raise ValidationError('Invalid business hours format')

        # Validate SMTP settings
        if self.smtp_settings:
            required_fields = ['host', 'port', 'username', 'password']
            for field in required_fields:
                if field not in self.smtp_settings:
                    raise ValidationError(f'Missing required SMTP field: {field}')

    def to_json(self):
        """Convert settings to JSON representation"""
        return {
            'id': self.id,
            'pharmacy_name': self.pharmacy.pharmacy_name,
            'business_name': self.business_name,
            'contact_email': self.contact_email,
            'contact_phone': self.contact_phone,
            'address': self.address,
            'business_hours': self.business_hours,
            'enable_notifications': self.enable_notifications,
            'low_stock_threshold': self.low_stock_threshold,
            'require_prescription_approval': self.require_prescription_approval,
            'auto_order_enabled': self.auto_order_enabled,
            'default_tax_rate': str(self.default_tax_rate),
            'currency': self.get_currency_display(),
            'language': self.get_language_display(),
            'timezone': self.timezone,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def get_business_hours_display(self):
        """Return formatted business hours"""
        if not self.business_hours:
            return "Not set"
        
        formatted_hours = []
        for day, hours in self.business_hours.items():
            formatted_hours.append(f"{day.capitalize()}: {hours['open']} - {hours['close']}")
        return "\n".join(formatted_hours)

    def get_smtp_config(self):
        """Return SMTP configuration with masked password"""
        if not self.smtp_settings:
            return None
        
        config = self.smtp_settings.copy()
        if 'password' in config:
            config['password'] = '********'
        return config

    @property
    def currency_symbol(self):
        """Return currency symbol based on currency choice"""
        return dict(self.CURRENCY_CHOICES).get(self.currency, '$')
    
 