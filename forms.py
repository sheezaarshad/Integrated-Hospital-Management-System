from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import Patients, Doctor, Appointment, Pharmacy, Order, Laboratory, TestReport, SampleCollectionRequest, Rider, Hospital, LabRider, PharmacyRider
class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('Patient', 'Patient'),
        ('Doctor', 'Doctor'),
        ('Hospital Owner', 'Hospital Owner'),
        ('Rider', 'Rider'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data['role']
        if commit:
            user.save()
            # Assign the user to the selected role group
            group = Group.objects.get(name=role)
            user.groups.add(group)
        return user

class PatientSignUpForm(UserCreationForm):
    patient_name = forms.CharField(max_length=100)
    dob = forms.DateField(widget=forms.SelectDateWidget(years=range(1950, 2024)))
    age = forms.IntegerField()
    phone = forms.CharField(max_length=15)
    email = forms.EmailField()
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    address = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ('username', 'patient_name', 'dob', 'age', 'phone', 'email', 'gender', 'address', 'password1', 'password2')

class DoctorSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # Use 'name' to match the Doctor model field
    name = forms.CharField(max_length=100)
    specialty = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=15)
    hospital = forms.ModelChoiceField(queryset=Hospital.objects.all())
    profile_image = forms.ImageField(required=False)
    available_days = forms.CharField(max_length=100)
    available_from = forms.TimeField()
    available_to = forms.TimeField()

    def save(self, commit=True):
        # Save the user (with username, email, and password)
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        # Save the doctor profile
        doctor = Doctor(
            user=user,
            name=self.cleaned_data['name'],  # Use 'name' instead of 'doctor_name'
            specialty=self.cleaned_data['specialty'],
            phone=self.cleaned_data['phone'],
            email=self.cleaned_data['email'],
            hospital=self.cleaned_data['hospital'],
            profile_image=self.cleaned_data.get('profile_image', None),
            available_days=self.cleaned_data['available_days'],
            available_from=self.cleaned_data['available_from'],
            available_to=self.cleaned_data['available_to']
        )
        if commit:
            doctor.save()
        return user


class HospitalOwnerSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True)

    # Fields for Hospital model
    hospital_name = forms.CharField(max_length=50, required=True)
    about_hospital = forms.CharField(widget=forms.Textarea, required=True)
    services_offered = forms.MultipleChoiceField(choices=[
        ("Emergency Services", "Emergency Services"),
        ("Surgical Services", "Surgical Services"),
        ("Medical Services", "Medical Services"),
        ("Diagnostic Services", "Diagnostic Services"),
        ("Therapeutic Services", "Therapeutic Services"),
        ("Outpatient Services", "Outpatient Services"),
        ("Inpatient Services", "Inpatient Services"),
        ("Maternity and Neonatal Care", "Maternity and Neonatal Care"),
        ("Pharmacy Services", "Pharmacy Services"),
        ("Mental Health Services", "Mental Health Services"),
    ], widget=forms.CheckboxSelectMultiple, required=True)
    domain_available = forms.MultipleChoiceField(choices=[
        ("Cardiology", "Cardiology"),
        ("Neurology", "Neurology"),
        ("Orthopedics", "Orthopedics"),
        ("Pediatrics", "Pediatrics"),
        ("Oncology", "Oncology"),
        ("Gynecology", "Gynecology"),
        ("Gastroenterology", "Gastroenterology"),
        ("Radiology", "Radiology"),
        ("Pathology", "Pathology"),
        ("Pharmacy", "Pharmacy"),
        ("Anesthesiology", "Anesthesiology"),
        ("Human Resources", "Human Resources"),
        ("Information Technology", "Information Technology"),
        ("Facilities Management", "Facilities Management"),
    ], widget=forms.CheckboxSelectMultiple, required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)
    image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

        hospital = Hospital(
            hospital_name=self.cleaned_data['hospital_name'],
            phone=self.cleaned_data['phone'],
            email=self.cleaned_data['email'],
            about_hospital=self.cleaned_data['about_hospital'],
            services_offered=", ".join(self.cleaned_data['services_offered']),
            domain_available=", ".join(self.cleaned_data['domain_available']),
            address=self.cleaned_data['address'],
            image=self.cleaned_data.get('image', None)
        )
        if commit:
            hospital.save()

        return user

class DoctorForm(forms.ModelForm):
    available_from = forms.TimeField(
        widget=forms.TimeInput(format='%I:%M %p'),
        input_formats=['%I:%M %p'],
        help_text="Start time in HH:MM AM/PM"
    )
    available_to = forms.TimeField(
        widget=forms.TimeInput(format='%I:%M %p'),
        input_formats=['%I:%M %p'],
        help_text="End time in HH:MM AM/PM"
    )

    class Meta:
        model = Doctor
        fields = ['name', 'specialty', 'phone', 'email', 'hospital', 'profile_image', 'available_days', 'available_from', 'available_to']
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient_name', 'date', 'time', 'reason']

    def __init__(self, *args, **kwargs):
        time_slots = kwargs.pop('time_slots', [])
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.fields['time'] = forms.ChoiceField(choices=[(slot, slot) for slot in time_slots], widget=forms.Select(attrs={'class': 'form-control'}))
        self.fields['patient_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['date'].widget.attrs.update({'class': 'form-control', 'type': 'date'})
        self.fields['reason'].widget.attrs.update({'class': 'form-control'})

class CancellationForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea, required=True)
class PharmacyForm(forms.ModelForm):
    class Meta:
        model = Pharmacy
        fields = ['pharmacy_name', 'phone', 'email', 'address']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'medicine_name', 'quantity', 'address', 'phone', 'email', 'dosage', 'form', 'prescription']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['customer_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Customer Name'})
        self.fields['medicine_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Medicine Name'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Quantity'})
        self.fields['address'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Address'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Phone'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
        self.fields['dosage'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Dosage (e.g. 500 mg)'})
        self.fields['form'].widget.attrs.update({'class': 'form-control'})
        self.fields['prescription'].widget.attrs.update({'class': 'form-control-file'})
class LaboratoryForm(forms.ModelForm):
    class Meta:
        model = Laboratory
        fields = ['lab_name', 'phone', 'email', 'address']

class TestReportForm(forms.ModelForm):
    patient_profile = forms.ModelChoiceField(
        queryset=Patients.objects.all(),
        label='Patient',
        required=True
    )

    class Meta:
        model = TestReport
        fields = ['patient_profile', 'test_name', 'sample_collected_date', 'report_date', 'report_file']
class SampleCollectionRequestForm(forms.ModelForm):
    class Meta:
        model = SampleCollectionRequest
        fields = ['patient_name', 'address', 'phone', 'email', 'requested_date', 'sample_type', 'test_name', 'time']

    def __init__(self, *args, **kwargs):
        super(SampleCollectionRequestForm, self).__init__(*args, **kwargs)
        self.fields['patient_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Patient Name'})
        self.fields['address'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Address'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Phone'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
        self.fields['requested_date'].widget.attrs.update({'class': 'form-control', 'type': 'date'})
        self.fields['sample_type'].widget.attrs.update({'class': 'form-control'})
        self.fields['test_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Test Name'})
        self.fields['time'].widget.attrs.update({'class': 'form-control', 'type': 'time'})


class RiderSignupForm(UserCreationForm):
    rider_type = forms.ChoiceField(choices=[('Lab', 'Laboratory Rider'), ('Pharmacy', 'Pharmacy Rider')])
    name = forms.CharField(max_length=100, required=True)
    phone = forms.CharField(max_length=15, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'rider_type', 'name', 'phone', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']  # Ensure email is updated
        if commit:
            user.save()
        # Create Rider instance and link it to the User instance
        Rider.objects.create(
            user=user,
            name=self.cleaned_data['name'],
            phone=self.cleaned_data['phone'],
            email=self.cleaned_data['email'],
            rider_type=self.cleaned_data['rider_type']
        )
        return user  # Return the User instance, not Rider

class LabRiderForm(forms.ModelForm):
    class Meta:
        model = LabRider
        fields = ['lab', 'training_credentials']

    def __init__(self, *args, **kwargs):
        super(LabRiderForm, self).__init__(*args, **kwargs)
        self.fields['lab'].widget.attrs.update({'class': 'form-control'})
        self.fields['training_credentials'].widget.attrs.update({'class': 'form-control-file'})

class PharmacyRiderForm(forms.ModelForm):
    class Meta:
        model = PharmacyRider
        fields = ['pharmacy']