from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return self.email

class Doctor(models.Model):
    # 1. Basic Information
    name = models.CharField(max_length=255, verbose_name="Doctor Name")
    specialty = models.CharField(max_length=150, verbose_name="Specialty")
    bio = models.TextField(verbose_name="Biography", blank=True)
    image = models.CharField(max_length=255, help_text="Example: /drNourhan.png")
    
    # 2. Clinic Details
    clinic_number = models.CharField(max_length=50, blank=True, null=True)
    schedule = models.CharField(max_length=255, verbose_name="Work Schedule")
    
    # 3. Real-time Status (Matches your JSON)
    available = models.BooleanField(default=True, verbose_name="Is Available Now?")
    next_slot = models.CharField(max_length=100, default="الآن", verbose_name="Next Available Slot")
    queue_length = models.IntegerField(default=0, verbose_name="Current Queue")

    class Meta:
        verbose_name = "Hospital Doctor"
        verbose_name_plural = "Hospital Doctors"

    def __str__(self):
        # Using specialty here helps you identify doctors in the admin list
        return f"Dr. {self.name} ({self.specialty})"
    
class Appointment(models.Model):
    # Link to the Doctor model we created earlier
    doctor = models.ForeignKey(Doctor, models.CASCADE, related_name='appointments')
    
    # Booking Reference (e.g., SKH-1234)
    reference_id = models.CharField(max_length=20, unique=True)
    
    # Patient Info (from bookingData)
    patient_name = models.CharField(max_length=255)
    patient_phone = models.CharField(max_length=20)
    appointment_date = models.DateField()
    reason = models.TextField(blank=True)
    
    # Status tracking
    status = models.CharField(
        max_length=20, 
        default='Confirmed', 
        choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Completed', 'Completed')]
    )
    payment_status = models.CharField(max_length=20, default='Paid')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reference_id} - {self.patient_name}"
    
class News(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    summary = models.TextField()
    content = models.TextField(blank=True)
    image = models.CharField(max_length=255, help_text="Example: /minister-visit.png")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "News"
        ordering = ['-created_at']

    def __str__(self):
        return self.title