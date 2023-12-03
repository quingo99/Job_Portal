from .forms import UserRegistrationForm
from django.shortcuts import render, redirect


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            form.save()
            return redirect('login')
        else:
            print("form has errors")

    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})