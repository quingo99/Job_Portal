from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import ApplicantProfileForm, EmployerProfileForm, AddressForm, JobPostingForm
from .models import EmployerProfile, ApplicantProfile, User, Address, Job
from django.db.models import Q



def homepage(request):
    job_list = Job.objects.all()
    profile_id = 0
    job = request.GET.get('job', '')
    address = request.GET.get('address', '')
    if job:
        job_list = job_list.filter(
            Q(title__icontains=job) |
            Q(description__icontains=job) |
            Q(job_type__icontains=job) |
            Q(location__icontains=job) |
            Q(employer__name__icontains=job)
        )
    if address:
        job_list = job_list.filter(
            Q(address__zip__icontains = address)|
            Q(address__city__icontains = address)|
            Q(address__state__icontains = address))

    role = ""
    if request.user.is_authenticated:
        # Determine the type of profile based on the user's role
        if request.user.role == User.Role.Employer:
            profile_id = request.user.employer_profile.id
            role = "Employer"
        elif request.user.role == User.Role.Applicant:
            profile_id = request.user.applicant_profile.id
            role = "Applicant"
        else:
            profile_id = 0

    return render(request, 'mainpage/index.html', {'role': role, 'job_list': job_list})


def profile(request):
    role, profile_id = get_role_profileid(request)
    user_profile = None
    profile_form = None
    address_instance = None
    print(role)
    print(profile_id)
    if role == "Employer":
        user_profile = EmployerProfile.objects.get(id=profile_id)
        profile_form = EmployerProfileForm(request.POST or None, instance=user_profile)
    elif role == "Applicant":
        user_profile = ApplicantProfile.objects.get(id=profile_id)
        # Include request.FILES for ApplicantProfileForm
        profile_form = ApplicantProfileForm(request.POST or None, request.FILES or None, instance=user_profile)
    else:
        return redirect('home')

    # Check if user profile has an associated address
    if user_profile and user_profile.address:
        address_instance = user_profile.address
    address_form = AddressForm(request.POST or None, instance=address_instance)

    if request.method == "POST":
        if profile_form.is_valid() and address_form.is_valid():
            address_data = address_form.cleaned_data
            existing_address = checkAddress(address_data)
            if existing_address:
                user_profile.address = existing_address
            else:
                saved_address = address_form.save()
                user_profile.address = saved_address
            user_profile.save()
            return redirect('home')

    return render(request, 'mainpage/profile.html', {
        'profile_form': profile_form,
        'address_form': address_form,
    })


def job_posting(request):
    role, profile_id = get_role_profileid(request)
    print(role)
    if role != "Employer":
        return redirect('home')
    employer_profile = EmployerProfile.objects.get(id=profile_id)
    if (not employer_profile.is_verify):
        return redirect(reverse('home') + '?posting_job=fail')
    job_form = JobPostingForm(request.POST or None)
    address_form = AddressForm(request.POST or None)
    if request.method == "POST":
        if job_form.is_valid() and address_form.is_valid():
            address_data = address_form.cleaned_data
            existing_address = checkAddress(address_data)
            job_instance = job_form.save(commit=False)
            if existing_address:
                job_instance.address =  existing_address
            else:
                saved_address = address_form.save()
                job_instance.address = saved_address
            job_instance.employer = employer_profile
            job_instance.save()  # Save the job instance itself
            job_form.save_m2m()  # If there are many-to-many fields, you need to save them too
            return redirect('home')
    return render(request, 'mainpage/job_posting.html', {
        'job_form': job_form, 'address_form': address_form})


def job_update(request, job_id):
    job = Job.objects.get(pk=job_id)
    job_address = job.address
    role, profile_id = get_role_profileid(request)

    if role != "Employer":
        return redirect("home")

    job_form = JobPostingForm(request.POST or None, instance=job)
    address_form = AddressForm(request.POST or None, instance=job_address)

    if request.method == "POST":
        if job_form.is_valid() and address_form.is_valid():
            address_data = address_form.cleaned_data
            # Check if an existing address matches the form data
            existing_address = checkAddress(address_data)

            if existing_address:
                job.address = existing_address
            else:
                saved_address = address_form.save()
                job.address = saved_address

            job.save()  # Save the job with the new or existing address
            return redirect("job_listing")

    return render(request, 'mainpage/job_posting.html', {
        'job_form': job_form,
        'address_form': address_form
    })


def applicant_list(request, job_id):
    job = Job.objects.get(pk=job_id)
    applicants = job.applicants.all()
    return render(request, 'mainpage/applicant_list.html', {'applicants': applicants})
def job_detail(request, job_id):
    job = Job.objects.get(pk=job_id)
    role, profile_id = get_role_profileid(request)
    is_authorize = False
    if role == "Employer":
        if job.employer.id == profile_id:
            is_authorize = True
    if request.method == "POST":
        role, profile_id = get_role_profileid(request)
        if profile_id != 0 and role == "Applicant":
            applicant = ApplicantProfile.objects.get(id = profile_id)
            job.applicants.add(applicant)
            job.save()
            return redirect(reverse('home') + '?application=success')

    if job:
        return render(request, 'mainpage/detail.html', {"job": job, "role": role, "is_authorize": is_authorize})


def job_listing(request):
    role, profile_id = get_role_profileid(request)
    if role != "Employer":
        return redirect("home")
    job_list = Job.objects.filter(employer_id=profile_id)
    return render(request, 'mainpage/job_listing.html', {"job_list": job_list})
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


def checkAddress(address_data):
    existing_address = Address.objects.filter(
        street=address_data['street'],
        city=address_data['city'],
        zip=address_data['zip'],
        state=address_data['state']
    ).first()
    return  existing_address