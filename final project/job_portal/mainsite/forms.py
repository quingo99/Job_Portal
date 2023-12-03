from django import forms
from .models import EmployerProfile, ApplicantProfile, Address, Job
from django.forms import inlineformset_factory




class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street', 'city', 'state', 'zip']

class EmployerProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True, disabled=True)
    class Meta:
        model = EmployerProfile
        fields = ['name', 'phone', 'email', 'industry', 'company_size', 'found_date', 'company_url', 'description']  # Do not include the address here
    def __init__(self, *args, **kwargs):
        super(EmployerProfileForm, self).__init__(*args, **kwargs)
        # Set the initial value for email from the user instance
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email
class ApplicantProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True, disabled=True)

    class Meta:
        model = ApplicantProfile
        fields = ['first_name',  'last_name', 'birth_day', 'email', 'phone', 'linkedin_url', 'profile_picture', 'resume']

    def __init__(self, *args, **kwargs):
        super(ApplicantProfileForm, self).__init__(*args, **kwargs)
        # Set the initial value for email from the user instance
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email


class JobPostingForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["title", 'job_type', 'location',  'description', 'job_url']

