from django.core.files.base import ContentFile
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template

from .forms import ResumeForm, ExperienceFormSet, EducationFormSet, SkillFormSet, CertificationFormSet
import pdfkit
from django.http import  HttpResponse
from django.template import loader
from mainsite.models import User, ApplicantProfile
# Create your views here.


from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import ResumeForm, ExperienceFormSet, EducationFormSet, SkillFormSet, CertificationFormSet
from .models import Resume, Education, Experience, Certification, Skill

def resume_create(request):
    role, user_id = get_role_profileid(request)
    print(role)
    if role != "Applicant":
        return redirect('home')

    if request.method == 'POST':
        resume_form = ResumeForm(request.POST, request.FILES)
        experience_formset = ExperienceFormSet(request.POST, request.FILES)
        education_formset = EducationFormSet(request.POST, request.FILES)
        skill_formset = SkillFormSet(request.POST, request.FILES)
        certification_formset = CertificationFormSet(request.POST, request.FILES)

        if (resume_form.is_valid() and
            experience_formset.is_valid() and
            education_formset.is_valid() and
            skill_formset.is_valid() and
            certification_formset.is_valid()):
            # Check if the user already has a resume and delete it
            old_resume = Resume.objects.filter(user=request.user).first()
            if old_resume:
                old_resume.delete()

            # Save the new resume
            resume_instance = resume_form.save(commit=False)
            resume_instance.user = request.user
            resume_instance.save()

            # Save the formsets
            for formset in [experience_formset, education_formset, skill_formset, certification_formset]:
                formset.instance = resume_instance
                formset.save()
            resume(request)
            return redirect('profile')

    else:
        resume_form = ResumeForm()
        experience_formset = ExperienceFormSet(queryset=Experience.objects.none())
        education_formset = EducationFormSet(queryset=Education.objects.none())
        skill_formset = SkillFormSet(queryset=Skill.objects.none())
        certification_formset = CertificationFormSet(queryset=Certification.objects.none())

    return render(request, 'resume/resume_create.html', {
        'resume_form': resume_form,
        'experience_form': experience_formset,
        'education_form': education_formset,
        'skill_form': skill_formset,
        'certification_form': certification_formset
    })


def resume(request):
    role, user_id = get_role_profileid(request)
    if role != "Applicant":
        return redirect('home')
    user = ApplicantProfile.objects.get(pk=user_id)
    try:
        user_resume = Resume.objects.get(user=request.user)
    except Resume.DoesNotExist:
        return redirect('home')

    if user_resume:
        experiences = user_resume.experiences.all()
        education = user_resume.education.all()
        skills = user_resume.skills.all()
        certifications = user_resume.certifications.all()
    else:
        experiences = education = skills = certifications = []

    # Pass these objects to your template
    context = {
        'applicant_profile': user,
        'resume': user_resume,
        'experiences': experiences,
        'education': education,
        'skills': skills,
        'certifications': certifications
    }

    # Render HTML content
    template = get_template('resume/resume.html')
    html = template.render(context)

    # PDF generation options
    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        'enable-local-file-access': ""
    }

    # Generate PDF
    pdf = pdfkit.from_string(html, False, options)

    # Save PDF to ApplicantProfile
    filename = user.first_name + '_'+user.last_name+'resume.pdf'
    user.resume.save(filename, ContentFile(pdf), save=True)

    # Create HTTP response with PDF
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'

    return response

def get_role_profileid(request):
    profile_id = 0
    role = ""
    if request.user.is_authenticated:
        # Determine the type of profile based on the user's role
        if request.user.role == User.Role.Employer:
            profile_id = request.user.employer_profile.id
            role = "Employer"
        elif request.user.role == User.Role.Applicant:
            profile_id = request.user.applicant_profile.id
            role = "Applicant"

    return (role, profile_id)