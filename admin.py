from django.contrib import admin
from django import forms
from .models import Patients, Hospital, Doctor, Appointment, Pharmacy, Laboratory, TestReport, SampleCollectionRequest, Rider, Order, LabRider, PharmacyRider

class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'patient_name', 'dob', 'age', 'phone', 'email', 'gender', 'address')
    search_fields = ('user__username', 'patient_name', 'email')

    def user(self, obj):
        return obj.user.username

    user.short_description = 'Username'

class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialty', 'phone', 'email', 'hospital']

class HospitalAdmin(admin.ModelAdmin):
    list_display = ('hospital_name', 'phone', 'email', 'address', 'is_approved')
    search_fields = ('hospital_name', 'phone', 'email')
    list_filter = ('services_offered', 'domain_available', 'is_approved')
    actions = ['approve_hospitals']

    def approve_hospitals(self, request, queryset):
        queryset.update(is_approved=True)

    approve_hospitals.short_description = "Approve selected hospitals"

class TestReportAdminForm(forms.ModelForm):
    patient = forms.ModelChoiceField(
        queryset=Patients.objects.all(),
        label='Patient',
        required=True
    )
    laboratory = forms.ModelChoiceField(
        queryset=Laboratory.objects.all(),
        label='Laboratory',
        required=False,
    )

    class Meta:
        model = TestReport
        fields = ['patient', 'test_name', 'sample_collected_date', 'report_date', 'report_file', 'laboratory']

class TestReportAdmin(admin.ModelAdmin):
    form = TestReportAdminForm
    list_display = ('test_name', 'patient', 'report_date', 'status', 'laboratory')
    list_filter = ('status', 'report_date')
    search_fields = ('test_name', 'patient__user__username')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(patient__user=request.user)
        return qs

    def save_model(self, request, obj, form, change):
        if not change:
            obj.save()
class SampleCollectionRequestAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'laboratory', 'requested_date', 'status', 'rider')
    list_filter = ('status',)
    search_fields = ('patient_name', 'laboratory__lab_name')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'rider':
            obj_id = request.resolver_match.kwargs.get('object_id')
            if obj_id:
                sample_request = SampleCollectionRequest.objects.get(id=obj_id)
                kwargs['queryset'] = Rider.objects.filter(labrider__lab=sample_request.laboratory)
            else:
                kwargs['queryset'] = Rider.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'medicine_name', 'quantity', 'pharmacy', 'address', 'phone', 'email', 'rider')
    search_fields = ('customer_name', 'medicine_name', 'pharmacy__pharmacy_name')
    list_filter = ('pharmacy', 'rider')
    list_editable = ('rider',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'rider':
            obj_id = request.resolver_match.kwargs.get('object_id')
            if obj_id:
                order = Order.objects.get(id=obj_id)
                kwargs['queryset'] = Rider.objects.filter(pharmacyrider__pharmacy=order.pharmacy)
            else:
                kwargs['queryset'] = Rider.objects.none()  
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class LabRiderAdmin(admin.ModelAdmin):
    list_display = ('get_rider_username', 'get_rider_email', 'get_lab_name', 'training_credentials')

    def get_rider_username(self, obj):
        return obj.rider.user.username

    def get_rider_email(self, obj):
        return obj.rider.user.email

    def get_lab_name(self, obj):
        return obj.lab.lab_name if obj.lab else None

    get_rider_username.short_description = 'Rider Username'
    get_rider_email.short_description = 'Rider Email'
    get_lab_name.short_description = 'Lab Name'

class PharmacyRiderAdmin(admin.ModelAdmin):
    list_display = ('get_rider_username', 'get_rider_email', 'get_pharmacy_name')

    def get_rider_username(self, obj):
        return obj.rider.user.username

    def get_rider_email(self, obj):
        return obj.rider.user.email

    def get_pharmacy_name(self, obj):
        return obj.pharmacy.pharmacy_name if obj.pharmacy else None

    get_rider_username.short_description = 'Rider Username'
    get_rider_email.short_description = 'Rider Email'
    get_pharmacy_name.short_description = 'Pharmacy Name'
class RiderAdmin(admin.ModelAdmin):
    list_display = ('get_user_username', 'get_user_email', 'rider_type', 'get_related_object')
    list_filter = ('rider_type',)
    search_fields = ('name', 'user__email', 'user__username')

    def get_user_email(self, obj):
        return obj.user.email

    get_user_email.short_description = 'Email'

    def get_user_username(self, obj):
        return obj.user.username

    get_user_username.short_description = 'username'

    def get_related_object(self, obj):
        if obj.rider_type == 'Lab':
            lab_rider = LabRider.objects.filter(rider=obj).first()
            return lab_rider.lab.lab_name if lab_rider and lab_rider.lab else None
        elif obj.rider_type == 'Pharmacy':
            pharmacy_rider = PharmacyRider.objects.filter(rider=obj).first()
            return pharmacy_rider.pharmacy.pharmacy_name if pharmacy_rider and pharmacy_rider.pharmacy else None
        return None

    get_related_object.short_description = 'Related Object'

admin.site.register(Patients, PatientAdmin)
admin.site.register(Hospital, HospitalAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Appointment)
admin.site.register(Pharmacy)
admin.site.register(Order, OrderAdmin)
admin.site.register(Laboratory)
admin.site.register(TestReport, TestReportAdmin)
admin.site.register(SampleCollectionRequest, SampleCollectionRequestAdmin)
admin.site.register(Rider, RiderAdmin)
admin.site.register(LabRider, LabRiderAdmin)
admin.site.register(PharmacyRider, PharmacyRiderAdmin)