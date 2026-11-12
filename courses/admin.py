import threading
from django.contrib import admin
from django import forms
from django.core.mail import send_mail
from django.conf import settings
from .models import (
    HeroSection, HeroFeaturedCard, Feature, PremiumResource, 
    Course, CourseSlot, CourseLearningPoint, SuccessStory, FAQ, AboutPageContent, 
    Enrollment, PaymentSetting
)

class SingletonAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not self.model.objects.exists()
    def has_delete_permission(self, request, obj=None):
        return False

class CourseLearningPointInline(admin.TabularInline):
    model = CourseLearningPoint
    extra = 3

class CourseAdmin(admin.ModelAdmin):
    inlines = [CourseLearningPointInline]
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'subtitle')  # Required for autocomplete_fields

class CourseSlotAdminForm(forms.ModelForm):
    class Meta:
        model = CourseSlot
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'vDateField'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'vDateField'}),
        }

@admin.register(CourseSlot)
class CourseSlotAdmin(admin.ModelAdmin):
    form = CourseSlotAdminForm
    list_display = ('course', 'slot_name', 'start_date', 'end_date', 'timing_info', 'max_capacity')
    list_filter = ('course', 'timing_info', 'start_date')
    search_fields = ('slot_name', 'course__title')

# Registering standard singleton/standard models
admin.site.register(HeroSection, SingletonAdmin)
admin.site.register(Feature)
admin.site.register(PremiumResource)
admin.site.register(Course, CourseAdmin)
admin.site.register(SuccessStory)
admin.site.register(FAQ)
admin.site.register(AboutPageContent, SingletonAdmin)

@admin.register(HeroFeaturedCard)
class HeroFeaturedCardAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'is_active', 'button_text')
    list_editable = ('is_active',)  # Allows turning it on/off with one click from the list view!
    autocomplete_fields = ['course']

    def has_add_permission(self, request):
        return not HeroFeaturedCard.objects.exists()
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(PaymentSetting)
class PaymentSettingAdmin(admin.ModelAdmin):
    list_display = ('upi_id', 'bank_account_name', 'bank_account_number', 'bank_ifsc')
    
    def has_add_permission(self, request):
        return not PaymentSetting.objects.exists()

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'course_title', 'assigned_slot', 'mobile_number', 'upi_transaction_id', 'amount_paid', 'verified', 'created_at')
    list_filter = ('verified', 'assigned_slot', 'created_at')
    search_fields = ('full_name', 'email', 'mobile_number', 'upi_transaction_id', 'course_title')
    list_editable = ('verified', 'assigned_slot') # Allows assigning slots and verifying directly from the list view!
    actions = ['approve_and_notify_students']

    def save_model(self, request, obj, form, change):
        send_email_flag = False
        if obj.verified:
            if change:
                old_obj = Enrollment.objects.get(pk=obj.pk)
                if not old_obj.verified or old_obj.assigned_slot != obj.assigned_slot:
                    send_email_flag = True
            else:
                send_email_flag = True

        super().save_model(request, obj, form, change)
        
        if send_email_flag:
            # Send email in a background thread so SQLite database unlocks immediately
            threading.Thread(target=self.send_confirmation_email, args=(obj,)).start()

    def send_confirmation_email(self, enrollment):
        slot_info = (
            f"Batch Slot: {enrollment.assigned_slot.slot_name} "
            f"({enrollment.assigned_slot.timing_info}, Starts: {enrollment.assigned_slot.start_date})"
            if enrollment.assigned_slot else "Batch Slot: To be assigned shortly"
        )
        
        subject = f"Enrollment Confirmed: {enrollment.course_title} - AspireFounder"
        message = (
            f"Hi {enrollment.full_name},\n\n"
            f"Great news! Your payment (UTR: {enrollment.upi_transaction_id or 'N/A'}) for "
            f"'{enrollment.course_title}' has been successfully verified.\n\n"
            f"Schedule Details:\n"
            f"- {slot_info}\n\n"
            f"You are now officially enrolled. Our team will share your portal login "
            f"and session details via WhatsApp ({enrollment.mobile_number}) and Email shortly.\n\n"
            f"Welcome aboard!\n"
            f"Team AspireFounder"
        )
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [enrollment.email],
                fail_silently=False,
            )
            print(f"--- ASYNCHRONOUS EMAIL DISPATCH SUCCESS FOR {enrollment.email} ---")
        except Exception as e:
            print(f"Error sending email to {enrollment.email}: {e}")

    @admin.action(description="Approve payments & send confirmation email")
    def approve_and_notify_students(self, request, queryset):
        updated_count = 0
        for enrollment in queryset:
            if not enrollment.verified:
                enrollment.verified = True
                enrollment.save()
                updated_count += 1
                threading.Thread(target=self.send_confirmation_email, args=(enrollment,)).start()

        self.message_user(request, f"Successfully approved {updated_count} student(s) and triggered confirmation emails.")