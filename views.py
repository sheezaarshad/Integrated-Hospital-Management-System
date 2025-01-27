from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from app.models import Patients, Hospital, Doctor, Appointment, Pharmacy, Order, Laboratory, TestReport, SampleCollectionRequest, Rider, LabRider, PharmacyRider
from .forms import CancellationForm, HospitalOwnerSignupForm, DoctorForm,DoctorSignupForm, AppointmentForm, PharmacyForm, OrderForm, LaboratoryForm, TestReportForm, SampleCollectionRequestForm, RiderSignupForm, LabRiderForm, PharmacyRiderForm, PatientSignUpForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Group, User
from .forms import CustomUserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from datetime import datetime, timedelta
import calendar

def BASE(request):
    is_doctor = False
    is_hospital_owner = False
    is_rider = False

    if request.user.is_authenticated:
        is_doctor = request.user.groups.filter(name='Doctor').exists()
        is_hospital_owner = request.user.groups.filter(name='Hospital Owner').exists()
        is_rider = request.user.groups.filter(name='Rider').exists()  # Check if user is a rider

    return render(request, 'base.html', {
        'is_doctor': is_doctor,
        'is_hospital_owner': is_hospital_owner,
        'is_rider': is_rider,
    })
def signup_role(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        if role == 'patient':
            return redirect('patient_signup')
        elif role == 'doctor':
            return redirect('doctor_signup')
        elif role == 'hospital_owner':
            return redirect('hospital_owner_signup')
        elif role == 'rider':
            return redirect('rider_signup')
    return render(request, 'registration/signup.html')
def signup_view(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        if role == 'patient':
            form = PatientSignUpForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('registration/login')

    else:
        # For GET request, just render the signup page
        return render(request, 'registration/signup.html')


def patient_signup(request):
    if request.method == 'POST':
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # Create and save the user

            # Create a Patients object for the user
            Patients.objects.create(
                user=user,
                patient_name=form.cleaned_data['patient_name'],
                dob=form.cleaned_data['dob'],
                age=form.cleaned_data['age'],
                phone=form.cleaned_data['phone'],
                email=form.cleaned_data['email'],
                gender=form.cleaned_data['gender'],
                address=form.cleaned_data['address']
            )

            # Add the user to the 'Patient' group
            group = Group.objects.get(name='Patient')
            user.groups.add(group)

            login(request, user)  # Log the user in
            return redirect('base')  # Redirect to home or another page
    else:
        form = PatientSignUpForm()
    return render(request, 'registration/patient_signup.html', {'patient_form': form})

def patient_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.groups.filter(name='Patient').exists():
            return redirect('patient_signup')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def patient_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect to the appropriate page after login
            return redirect('base')  # Replace 'base' with your desired URL name
        else:
            # Set error message for invalid credentials
            messages.error(request, 'Invalid username or password.')
            return redirect('login')  # Redirect to the login page to show error message

    return render(request, 'registration/login.html')
@login_required
def patient_logout(request):
    logout(request)
    return redirect('base')


def add_Patients(request):
    if request.method == "POST":
        patient_name = request.POST.get('patient_name')
        dob = request.POST.get('dob')
        age = request.POST.get('age')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        address = request.POST.get('address')

        patients = Patients(
            patient_name=patient_name,
            date_of_birth=dob,
            age=age,
            Phone=phone,
            Email=email,
            Gender=gender,
            Address=address,
        )
        patients.save()

        return redirect('base')

    return render(request, 'Patients/add_patients.html')

def doctor_signup(request):
    if request.method == 'POST':
        form = DoctorSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()  # Save the user and doctor in one step
            group = Group.objects.get(name='Doctor')
            user.groups.add(group)
            login(request, user)
            return redirect('doctor_profile')  # Redirect to home after signup
    else:
        form = DoctorSignupForm()

    return render(request, 'registration/doctor_signup.html', {'doctor_form': form})

@login_required
def add_doctors(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES)
        if form.is_valid():
            doctor = form.save(commit=False)
            doctor.user = request.user  # Associate the logged-in user with the doctor
            doctor.save()
            return redirect('hospital_available')
    else:
        form = DoctorForm()
    return render(request, 'doctors/add_doctors.html', {'form': form})
def edit_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, pk=doctor_id)
    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('hospital_available')
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'doctors/edit_doctor.html', {'form': form})

def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctors/doctor_list.html', {'doctors': doctors})

def hospital_owner_signup(request):
    if request.method == 'POST':
        form = HospitalOwnerSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()  # Save the user and hospital data
            group = Group.objects.get(name='Hospital Owner')
            user.groups.add(group)
            return redirect('base')  # Redirect to home after signup
    else:
        form = HospitalOwnerSignupForm()

    return render(request, 'registration/hospital_owner_signup.html', {'hospital_owner_form': form})
@login_required
def add_hospital(request):
    services = [
        "Emergency Services", "Surgical Services", "Medical Services",
        "Diagnostic Services", "Therapeutic Services", "Outpatient Services",
        "Inpatient Services", "Maternity and Neonatal Care", "Pharmacy Services",
        "Mental Health Services"
    ]
    domains = [
        "Cardiology", "Neurology", "Orthopedics", "Pediatrics", "Oncology",
        "Gynecology", "Gastroenterology", "Radiology", "Pathology", "Pharmacy",
        "Anesthesiology", "Human Resources", "Information Technology", "Facilities Management"
    ]

    if request.method == "POST":
        hospital_name = request.POST.get('hospital_name')
        Phone = request.POST.get('Phone')
        email = request.POST.get('email')
        about_hospital = request.POST.get('about_hospital')
        services_offered = request.POST.getlist('services_offered')
        domain_available = request.POST.getlist('domain_available')
        address = request.POST.get('address')
        image = request.FILES.get('image')

        # Fix the indentation here
        new_hospital = Hospital(
            hospital_name=hospital_name,
            Phone=Phone,
            Email=email,
            About_Hospital=about_hospital,
            Services_Offered=", ".join(services_offered),
            Domain_Available=", ".join(domain_available),
            Address=address,
            image=image
        )
        new_hospital.save()

        return redirect('hospital_available')

    context = {
        'services': services,
        'domains': domains
    }
    return render(request, 'hospital/add_hospital.html', context)

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
        image=self.cleaned_data.get('image', None),
        user=user,
        is_approved=False
    )
    if commit:
        hospital.save()

    return user

def hospital_available(request):
    hospitals = Hospital.objects.filter(is_approved=True)
    return render(request, 'hospital/hospital_available.html', {'hospitals':hospitals})

def hospital_detail(request, hospital_id):
    hospital_obj = get_object_or_404(Hospital, pk=hospital_id)
    return render(request, 'hospital/hospital_detail.html', {'hospital': hospital_obj})

@patient_required
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    patient_profile = get_object_or_404(Patients, user=request.user)  # Get patient profile for logged-in user

    # Generate available time slots in 24-hour format
    time_slots = []
    current_time = datetime.combine(datetime.today(), doctor.available_from)
    end_time = datetime.combine(datetime.today(), doctor.available_to)

    while current_time <= end_time:
        time_slots.append(current_time.strftime('%H:%M'))  # Use 24-hour format (HH:MM)
        current_time += timedelta(minutes=30)  # Assuming 30-minute intervals

    if request.method == 'POST':
        form = AppointmentForm(request.POST, time_slots=time_slots)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.doctor = doctor
            appointment.patient_name = patient_profile.patient_name  # Set the patient name from patient profile
            appointment.save()
            messages.success(request, 'Appointment booked successfully!')
            return redirect('hospital_detail', hospital_id=doctor.hospital.id)
    else:
        form = AppointmentForm(time_slots=time_slots)

    return render(request, 'appointment/book_appointment.html', {'form': form, 'doctor': doctor, 'time_slots': time_slots})

def appointment_success(request):
    return render(request, 'appointment/appointment_success.html')


@login_required
def appointment_detail(request, appointment_id):
    # Fetch the appointment regardless of the patient's name
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Render the appointment detail page for the logged-in user
    return render(request, 'appointment/appointment_detail.html', {
        'appointment': appointment
    })

@login_required
def cancel_appointment(request, appointment_id):
    # Fetch the appointment
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == 'POST':
        form = CancellationForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']
            appointment.delete()  # Delete the appointment
            messages.success(request, "Appointment canceled successfully.")
            return redirect('view_profile')
    else:
        form = CancellationForm()

    return render(request, 'appointment/cancel_appointment.html', {
        'form': form,
        'appointment': appointment
    })

def rider_signup(request):
    lab_rider_form = None
    pharmacy_rider_form = None
    laboratories = Laboratory.objects.all()
    pharmacies = Pharmacy.objects.all()

    if request.method == 'POST':
        rider_form = RiderSignupForm(request.POST)
        if 'training_credentials' in request.FILES:
            lab_rider_form = LabRiderForm(request.POST, request.FILES)
        else:
            lab_rider_form = LabRiderForm()

        if rider_form.is_valid() and lab_rider_form.is_valid():
            user = rider_form.save()
            rider_type = rider_form.cleaned_data['rider_type']
            rider = Rider.objects.get(user=user)

            if rider_type == 'Lab':
                lab_rider = lab_rider_form.save(commit=False)
                lab_rider.rider = rider
                lab_rider.save()
                group = Group.objects.get(name='Rider')
                user.groups.add(group)
            elif rider_type == 'Pharmacy':
                pharmacy_rider_form = PharmacyRiderForm(request.POST)
                if pharmacy_rider_form.is_valid():
                    pharmacy_rider = pharmacy_rider_form.save(commit=False)
                    pharmacy_rider.rider = rider
                    pharmacy_rider.save()
                    group = Group.objects.get(name='Rider')
                    user.groups.add(group)

            login(request, user)
            return redirect('base')
    else:
        rider_form = RiderSignupForm()
        lab_rider_form = LabRiderForm()
        pharmacy_rider_form = PharmacyRiderForm()

    return render(request, 'registration/rider_signup.html', {
        'rider_form': rider_form,
        'lab_rider_form': lab_rider_form,
        'pharmacy_rider_form': pharmacy_rider_form,
        'laboratories': laboratories,
        'pharmacies': pharmacies
    })
def add_pharmacy(request, hospital_id):
    hospital = get_object_or_404(Hospital, id=hospital_id)
    if request.method == 'POST':
        form = PharmacyForm(request.POST)
        if form.is_valid():
            pharmacy = form.save(commit=False)
            pharmacy.hospital = hospital
            pharmacy.save()
            messages.success(request, 'Pharmacy added successfully!')
            return redirect('hospital_detail', hospital_id=hospital_id)
    else:
        form = PharmacyForm()
    return render(request, 'pharmacy/add_pharmacy.html', {'form': form, 'hospital': hospital})
@patient_required
def order_medicine(request, pharmacy_id):
    pharmacy = get_object_or_404(Pharmacy, pk=pharmacy_id)
    patient_profile = get_object_or_404(Patients, user=request.user)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.pharmacy = pharmacy
            order.customer_name = patient_profile.patient_name  # Set the customer's name
            order.save()
            messages.success(request, 'Order placed successfully!')
            return redirect('view_profile')  # Redirect to profile page to see the order
    else:
        form = OrderForm()

    return render(request, 'pharmacy/order_medicine.html', {'form': form, 'pharmacy': pharmacy})
def add_laboratory(request, hospital_id):
    hospital = get_object_or_404(Hospital, id=hospital_id)
    if request.method == 'POST':
        form = LaboratoryForm(request.POST)
        if form.is_valid():
            laboratory = form.save(commit=False)
            laboratory.hospital = hospital
            laboratory.save()
            messages.success(request, 'Laboratory added successfully!')
            return redirect('hospital_detail', hospital_id=hospital_id)
    else:
        form = LaboratoryForm()
    return render(request, 'laboratory/add_laboratory.html', {'form': form, 'hospital': hospital})

def admin_sample_requests(request):
    sample_requests = SampleCollectionRequest.objects.filter(status='Pending')
    return render(request, 'admin/sample_requests.html', {'sample_requests': sample_requests})

def assign_rider(request, sample_request_id):
    sample_request = get_object_or_404(SampleCollectionRequest, id=sample_request_id)
    lab_riders = Rider.objects.filter(labrider__lab=sample_request.laboratory)

    if request.method == 'POST':
        rider_id = request.POST.get('rider')
        rider = get_object_or_404(Rider, id=rider_id)
        sample_request.rider = rider
        sample_request.status = 'Completed'
        sample_request.save()
        messages.success(request, 'Rider assigned successfully!')
        return redirect('admin_sample_requests')

    return render(request, 'laboratory/assign_rider.html', {'sample_request': sample_request, 'riders': lab_riders})

def pharmacy_available(request):
    pharmacies = Pharmacy.objects.all()
    return render(request, 'pharmacy/pharmacy_available.html', {'pharmacies': pharmacies})


def labs_available(request):
    laboratories = Laboratory.objects.all()
    return render(request, 'Laboratory/labs_available.html', {'laboratories': laboratories})

def add_test_report(request):
    if request.method == 'POST':
        form = TestReportForm(request.POST, request.FILES)
        if form.is_valid():
            test_report = form.save(commit=False)
            # Admin selects the patient profile manually
            patient_profile_id = request.POST.get('patient_profile')
            try:
                patient_profile = Patients.objects.get(id=patient_profile_id)
                test_report.patient = patient_profile
                test_report.save()
                return redirect('view_test_reports')
            except Patients.DoesNotExist:
                form.add_error(None, 'Selected patient does not exist.')
    else:
        form = TestReportForm()
        # Fetch all patient profiles for admin to select
        patients = Patients.objects.all()

    return render(request, 'add_test_report.html', {
        'form': form,
        'Patients': Patients,
    })
@patient_required
def request_sample_collection(request, laboratory_id):
    laboratory = get_object_or_404(Laboratory, id=laboratory_id)
    patient_profile = get_object_or_404(Patients, user=request.user)

    if request.method == 'POST':
        form = SampleCollectionRequestForm(request.POST)
        if form.is_valid():
            sample_request = form.save(commit=False)
            sample_request.laboratory = laboratory
            sample_request.patient_name = patient_profile.patient_name  # Ensuring patient name consistency
            sample_request.save()
            messages.success(request, 'Sample collection request submitted successfully!')
            return redirect('hospital_detail', hospital_id=laboratory.hospital.id)
    else:
        form = SampleCollectionRequestForm()

    return render(request, 'laboratory/request_sample_collection.html', {'form': form, 'laboratory': laboratory})

def add_rider(request):
    return render(request, 'rider/add_rider.html')

def submit_rider_form(request):
    if request.method == 'POST':
        form = RiderForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page or another appropriate view
            return redirect('base')  # Redirect to base.html or another page
    else:
        form = RiderForm()

    return render(request, 'rider/add_rider.html', {'form': form})

@patient_required
def view_test_reports(request, laboratory_id):
    # Filter test reports based on the laboratory_id if needed
    laboratory = get_object_or_404(Laboratory, id=laboratory_id)
    test_reports = TestReport.objects.filter(laboratory=laboratory)

    context = {
        'test_reports': test_reports,
        'laboratory': laboratory,  # Pass the laboratory to the template if needed
    }
    return render(request, 'Laboratory/view_test_reports.html', context)


@login_required
def view_profile(request):
    try:
        # Assuming 'Patients' is the model you are using for patient profiles
        patient_profile = Patients.objects.get(user=request.user)  # Get profile for the logged-in user
    except Patients.DoesNotExist:
        # Redirect if the patient's profile doesn't exist
        messages.error(request, "Patient profile not found. Please create your patient profile.")
        return redirect('add_patients')  # Change this to the correct URL for adding a patient profile

    # Get related data for the patient
    appointments = Appointment.objects.filter(patient_name=patient_profile.patient_name)
    orders = Order.objects.filter(customer_name=patient_profile.patient_name)
    test_reports = TestReport.objects.filter(patient=patient_profile)
    sample_collection_requests = SampleCollectionRequest.objects.filter(patient_name=patient_profile.patient_name)

    context = {
        'profile': patient_profile,
        'appointments': appointments,
        'orders': orders,
        'test_reports': test_reports,
        'sample_collection_requests': sample_collection_requests,
    }

    return render(request, 'Patients/patient_profile_view.html', context)

@login_required
def doctor_profile_view(request):
    # Get the logged-in user's doctor profile
    doctor = get_object_or_404(Doctor, user=request.user)

    # Get appointments for the logged-in doctor
    appointments = Appointment.objects.filter(doctor=doctor)

    return render(request, 'doctors/doctor_profile_view.html', {
        'doctor': doctor,
        'appointments': appointments,
    })

@login_required
def cancel_appointment_doctor(request, appointment_id):
    # Get the appointment object
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor__user=request.user)

    # Ensure the doctor can only delete their own appointments
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'The appointment has been successfully cancelled.')
        return redirect('doctor_profile')  # Correct URL name here

    return render(request, 'appointment/confirm_cancel_appointment.html', {'appointment': appointment})


@login_required
def hospital_owner_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    hospital = get_object_or_404(Hospital, user=request.user)

    doctors = Doctor.objects.filter(hospital=hospital)
    labs = Laboratory.objects.filter(hospital=hospital)
    pharmacies = Pharmacy.objects.filter(hospital=hospital)

    context = {
        'hospital': hospital,
        'doctors': doctors,
        'labs': labs,
        'pharmacies': pharmacies,
    }

    return render(request, 'hospital/hospital_owner_profile.html', context)

@login_required
def rider_profile(request):
    rider = Rider.objects.get(user=request.user)  # Fetch the logged-in rider
    sample_collection_requests = []
    orders = []

    if rider.rider_type == 'Lab':
        # Get all sample collection requests assigned to this lab rider
        sample_collection_requests = SampleCollectionRequest.objects.filter(rider=rider)
    elif rider.rider_type == 'Pharmacy':
        # Get all pharmacy orders assigned to this pharmacy rider
        orders = Order.objects.filter(rider=rider)

    return render(request, 'rider/rider_profile.html', {
        'rider': rider,
        'sample_collection_requests': sample_collection_requests,
        'orders': orders,
    })
