from django.db import models
from django.contrib.auth.models import User
import datetime
from django.conf import settings
from django.utils import timezone
from django.core.validators import FileExtensionValidator

class Patients(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)  # Temporarily nullable
    patient_name = models.CharField(max_length=100)
    dob = models.DateField(default=timezone.now)
    age = models.IntegerField()
    phone = models.CharField(max_length=15, default='0000000000')
    email = models.EmailField(max_length=100)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], default='Not Specified')
    address = models.TextField()

    def __str__(self):
        return self.user.username

class Hospital(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    hospital_name = models.CharField(max_length=50)
    phone = models.IntegerField()
    email = models.EmailField(max_length=100)
    about_hospital = models.TextField()
    services_offered = models.TextField()
    domain_available = models.TextField()
    address = models.TextField()
    image = models.ImageField(upload_to='hospital_images/', null=True, blank=True)
    is_approved = models.BooleanField(default=False)


    def __str__(self):
        return self.hospital_name

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    hospital = models.ForeignKey(Hospital, related_name='doctors', on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='doctor_profiles/', null=True, blank=True)
    available_days = models.CharField(max_length=100, default="", help_text="Enter days like Monday, Tuesday, etc.")
    available_from = models.TimeField(default="", help_text="Start time in HH:MM AM/PM")
    available_to = models.TimeField(default="", help_text="End time in HH:MM AM/PM")

    def __str__(self):
        return self.name

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=100, default="")
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField()

    def __str__(self):
        return f"Appointment with {self.doctor.name} on {self.date} at {self.time}"

class Pharmacy(models.Model):
    pharmacy_name = models.CharField(max_length=100)
    hospital = models.ForeignKey(Hospital, related_name='pharmacies', on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.pharmacy_name

class Laboratory(models.Model):
    hospital = models.OneToOneField(Hospital, related_name='laboratory', on_delete=models.CASCADE)
    lab_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.lab_name

def get_default_patient():
    return Patients.objects.first()

class TestReport(models.Model):
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=100)
    sample_collected_date = models.DateField(default=datetime.date.today)
    report_date = models.DateField(default=datetime.date.today)
    report_file = models.FileField(upload_to='reports/', null=True, blank=True)
    laboratory = models.ForeignKey(Laboratory, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Completed', 'Completed')])
    def __str__(self):
        return f"Test Report for {self.patient.user.username} - {self.test_name}"

class Rider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    rider_type = models.CharField(max_length=10, choices=[('Lab', 'Laboratory'), ('Pharmacy', 'Pharmacy')])

    def __str__(self):
        return self.name
class LabRider(models.Model):
    rider = models.OneToOneField(Rider, on_delete=models.CASCADE)
    lab = models.ForeignKey('Laboratory', on_delete=models.SET_NULL, null=True, blank=True)
    training_credentials = models.FileField(upload_to='training_credentials/', blank=True, null=True)

    def __str__(self):
        return f"{self.rider.name} - Lab Rider"

class PharmacyRider(models.Model):
    rider = models.OneToOneField(Rider, on_delete=models.CASCADE)
    pharmacy = models.ForeignKey('Pharmacy', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.rider.name} - Pharmacy Rider"
class SampleCollectionRequest(models.Model):
    SAMPLE_TYPES = [
        ('Blood', 'Blood'),
        ('Urine', 'Urine'),
        ('Other', 'Other'),
    ]

    laboratory = models.ForeignKey(Laboratory, related_name='sample_requests', on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    requested_date = models.DateField()
    sample_type = models.CharField(max_length=50, choices=SAMPLE_TYPES, default='Blood')
    test_name = models.CharField(max_length=100 , default='')
    time = models.TimeField(default=' ')
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending')
    rider = models.ForeignKey(Rider, related_name='requests', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Sample collection request from {self.patient_name}"

class Order(models.Model):
    FORM_CHOICES = [
        ('tablet', 'Tablet'),
        ('syrup', 'Syrup'),
        ('injection', 'Injection'),
        ('cream', 'Cream'),
        ('other', 'Other'),
    ]

    pharmacy = models.ForeignKey(Pharmacy, related_name='orders', on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    medicine_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    dosage = models.CharField(max_length=50, blank=True, null=True)
    form = models.CharField(max_length=10, choices=FORM_CHOICES, default='tablet')
    prescription = models.FileField(upload_to='prescriptions/', blank=True, null=True)
    rider = models.ForeignKey(Rider, related_name='orders', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Order for {self.medicine_name} by {self.customer_name}"