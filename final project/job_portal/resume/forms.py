from django import forms
from django.forms import inlineformset_factory

from .models import Resume, Experience, Education, Skill, Certification

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['first_name', 'last_name', 'email', 'phone','linkedIn', 'summary']
        widgets = {
            'summary': forms.Textarea(attrs={'placeholder': 'Enter a brief summary about yourself'}),
        }

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['title', 'company', 'start_date', 'end_date', 'description']

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['institution', 'degree', 'field_of_study', 'start_date', 'end_date', 'description']

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['skill_name', 'description']

class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = ['name', 'issuing_organization', 'issue_date', 'expiration_date', 'credential_id', 'credential_url']


ExperienceFormSet = inlineformset_factory(Resume, Experience, form=ExperienceForm, extra=1)
EducationFormSet = inlineformset_factory(Resume, Education, form=EducationForm, extra=1)
SkillFormSet = inlineformset_factory(Resume, Skill, form=SkillForm, extra=1)
CertificationFormSet = inlineformset_factory(Resume, Certification, form=CertificationForm, extra=1)
