from django import forms
from .models import Enrollment

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['full_name', 'email', 'mobile_number', 'upi_transaction_id']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'w-full bg-background border border-border rounded-xl px-4 py-3 text-foreground focus:outline-none focus:border-primary', 'placeholder': 'Enter your full name'}),
            'email': forms.EmailInput(attrs={'class': 'w-full bg-background border border-border rounded-xl px-4 py-3 text-foreground focus:outline-none focus:border-primary', 'placeholder': 'name@example.com'}),
            'mobile_number': forms.TextInput(attrs={'class': 'w-full bg-background border border-border rounded-xl px-4 py-3 text-foreground focus:outline-none focus:border-primary', 'placeholder': '10-digit mobile number'}),
            'upi_transaction_id': forms.TextInput(attrs={'class': 'w-full bg-background border border-border rounded-xl px-4 py-3 text-foreground focus:outline-none focus:border-primary', 'placeholder': 'Enter 12-digit UPI Ref / UTR No. (Optional if paying via Bank)'}),
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

    def clean_upi_transaction_id(self):
        utr = self.cleaned_data.get('upi_transaction_id')
        # UTR is now optional, so if provided, clean and validate it lightly
        if utr:
            return utr.strip()
        return utr