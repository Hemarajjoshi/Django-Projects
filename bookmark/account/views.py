from django.shortcuts import render
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages



# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user =  authenticate(request, username = cd['username'], password= cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("<h2> Authenticated Successfully</h2>")

                else:
                    return HttpResponse("<h2> Disabled Account</h2>")
            else:
                return HttpResponse("<h2> Invalid Login</h2>")
    else:
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})
    

@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': dashboard} )




def signup(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit= False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user = new_user)
            messages.success(request, "User Registered Successfully ")
            return render(request, 'account/signup_done.html', {'new_user': new_user})
        else:
            messages.error(request, "Cannot Register your messages please Enter Valid details")
    else:
        user_form = UserRegistrationForm()
        return render(request, 'account/signup.html', {'user_form': user_form})
    



@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance = request.user, data= request.POST)
        profile_form = ProfileEditForm(instance = request.user.profile, data = request.POST, files = request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return render(request, 'account/edit_done.html')
    else:
        user_form = UserEditForm(instance = request.user)
        profile_form = ProfileEditForm(instance= request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})
    




        