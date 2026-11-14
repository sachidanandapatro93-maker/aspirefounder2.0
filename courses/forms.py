from django import forms
from .models import Enrollment

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = [
            'full_name', 'email', 'mobile_number', 'whatsapp_number', 
            'student_photo', 'id_proof', 'upi_transaction_id', 'payment_screenshot'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'w-full bg-slate-900 border border-slate-700 text-slate-100 rounded-xl px-4 py-3 focus:outline-none focus:border-emerald-400', 
                'placeholder': 'Enter your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full bg-slate-900 border border-slate-700 text-slate-100 rounded-xl px-4 py-3 focus:outline-none focus:border-emerald-400', 
                'placeholder': 'name@example.com'
            }),
            'mobile_number': forms.TextInput(attrs={
                'id': 'id_mobile_number',
                'class': 'w-full bg-slate-900 border border-slate-700 text-slate-100 rounded-xl px-4 py-3 focus:outline-none focus:border-emerald-400', 
                'placeholder': '10-digit mobile number'
            }),
            'whatsapp_number': forms.TextInput(attrs={
                'id': 'id_whatsapp_number',
                'class': 'w-full bg-slate-900 border border-slate-700 text-slate-100 rounded-xl px-4 py-3 focus:outline-none focus:border-emerald-400', 
                'placeholder': 'WhatsApp number'
            }),
            'student_photo': forms.ClearableFileInput(attrs={
                'id': 'id_student_photo',
                'class': 'w-full text-sm text-slate-300 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-sm file:font-semibold file:bg-emerald-500 file:text-slate-950 hover:file:bg-emerald-400 cursor-pointer'
            }),
            'id_proof': forms.ClearableFileInput(attrs={
                'class': 'w-full text-sm text-slate-300 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-sm file:font-semibold file:bg-emerald-500 file:text-slate-950 hover:file:bg-emerald-400 cursor-pointer'
            }),
            'upi_transaction_id': forms.TextInput(attrs={
                'class': 'w-full bg-slate-900 border border-slate-700 text-slate-100 rounded-xl px-4 py-3 focus:outline-none focus:border-emerald-400', 
                'placeholder': 'Enter 12-digit UPI Ref / UTR No. (Optional)'
            }),
            'payment_screenshot': forms.ClearableFileInput(attrs={
                'class': 'w-full text-sm text-slate-300 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-sm file:font-semibold file:bg-emerald-500 file:text-slate-950 hover:file:bg-emerald-400 cursor-pointer'
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Enrollment.objects.filter(email=email).exists():
            raise forms.ValidationError("An enrollment with this email address already exists.")
        return email

    def clean_mobile_number(self):
        mobile = self.cleaned_data.get('mobile_number')
        if not mobile:
            raise forms.ValidationError("Please enter a mobile number.")
        
        cleaned_mobile = "".join(filter(str.isdigit, mobile))
        if len(cleaned_mobile) < 10:
            raise forms.ValidationError("Please enter a valid 10-digit mobile number.")
            
        if Enrollment.objects.filter(mobile_number=mobile).exists():
            raise forms.ValidationError("An enrollment with this mobile number already exists.")
            
        return mobile

    def clean_whatsapp_number(self):
        whatsapp = self.cleaned_data.get('whatsapp_number')
        if not whatsapp:
            raise forms.ValidationError("Please enter a WhatsApp number.")
        return whatsapp.strip()

    def clean_student_photo(self):
        photo = self.cleaned_data.get('student_photo')
        if not photo:
            raise forms.ValidationError("Please upload a student photo.")
        return photo

    def clean_id_proof(self):
        proof = self.cleaned_data.get('id_proof')
        if not proof:
            raise forms.ValidationError("Please upload an ID proof document.")
        return proof

    def clean_payment_screenshot(self):
        screenshot = self.cleaned_data.get('payment_screenshot')
        if not screenshot:
            raise forms.ValidationError("Please upload a payment screenshot.")
        return screenshot

    def clean_upi_transaction_id(self):
        utr = self.cleaned_data.get('upi_transaction_id')
        if utr:
            return utr.strip()
        return ""