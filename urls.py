from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from app import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.BASE, name='base'),
    path('signup/', views.signup_view, name='signup'),
    path('signup/', views.signup_role, name='signup_role'),
    path('patient-signup/', views.patient_signup, name='patient_signup'),
    path('doctor-signup/', views.doctor_signup, name='doctor_signup'),
    path('hospital_owner_signup/', views.hospital_owner_signup, name='hospital_owner_signup'),
    path('hospital-owner-profile/', views.hospital_owner_profile, name='hospital_owner_profile'),
    path('rider_signup/', views.rider_signup, name='rider_signup'),
    path('login/', views.patient_login, name='login'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.patient_logout, name='logout'),
    path('view_profile/', views.view_profile, name='view_profile'),
    path('Patients/add/', views.add_Patients, name='add_patients'),
    path('hospital/add/', views.add_hospital, name='add_hospital'),
    path('hospital/available/', views.hospital_available, name='hospital_available'),
    path('hospital/<int:hospital_id>/', views.hospital_detail, name='hospital_detail'),
    path('doctors/add/', views.add_doctors, name='add_doctors'),
    path('doctors/edit/<int:doctor_id>/', views.edit_doctor, name='edit_doctor'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctor/profile/', views.doctor_profile_view, name='doctor_profile'),
    path('book-appointment/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('appointment/<int:appointment_id>/', views.appointment_detail, name='appointment_detail'),
    path('cancel_appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('doctor/appointment/cancel/<int:appointment_id>/', views.cancel_appointment_doctor,name='cancel_appointment_doctor'),
    path('hospital/<int:hospital_id>/add_pharmacy/', views.add_pharmacy, name='add_pharmacy'),
    path('pharmacy-available/', views.pharmacy_available, name='pharmacy_available'),
    path('order-medicine/<int:pharmacy_id>/', views.order_medicine, name='order_medicine'),
    path('pharmacy/<int:pharmacy_id>/order/', views.order_medicine, name='order_medicine_pharmacy'),
    path('hospital/<int:hospital_id>/add_laboratory/', views.add_laboratory, name='add_laboratory'),
    path('labs-available/', views.labs_available, name='labs_available'),
    path('laboratory/<int:laboratory_id>/view_test_reports/', views.view_test_reports,name='view_test_reports'),
    path('request-sample-collection/<int:laboratory_id>/', views.request_sample_collection, name='request_sample_collection'),
    path('admin-sample-requests/', views.admin_sample_requests, name='admin_sample_requests'),
    path('assign-rider/<int:sample_request_id>/', views.assign_rider, name='assign_rider'),
    path('add_rider/', views.add_rider, name='add_rider'),
    path('submit_rider_form/', views.submit_rider_form, name='submit_rider_form'),
    path('rider_profile/', views.rider_profile, name='rider_profile'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

