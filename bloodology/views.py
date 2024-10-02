from django.shortcuts import render,HttpResponseRedirect,redirect, get_object_or_404
from . forms import RequestPostForm,UserRegistrationForm,userLogin
from . models import BloodRequestPost, UserProfile
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request):
    reqPost = BloodRequestPost.objects.all().order_by('-created_at')
    userProfiles = UserProfile.objects.all() 
    return render(request, 'bloodology/home.html', {'posts': reqPost, 'profiles': userProfiles})

#SignUP

def user_signUp(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')  # Redirect to the login page if the form is valid
    else:
        form = UserRegistrationForm()  # Initialize the form for GET requests

    return render(request, 'bloodology/signUp.html', {'form': form})



#User Profile
@login_required
def user_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    return render(request, 'bloodology/user_profile.html',{'profile': profile})

#Blood Request Post
def AddRequestForm(request):
    form = RequestPostForm()  # Initialize the form at the start
    if request.method == "POST":
        form = RequestPostForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')  # Redirect after successful form submission
        else:
            form = RequestPostForm()

    return render(request, 'bloodology/AddRequestForm.html', {'form': form})

# Login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = userLogin(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    # Add a message for invalid login credentials
                    messages.error(request, 'Invalid username or password.')
            else:
                # Add a message if the form is not valid
                messages.error(request, "Invalid username or password.....")

        # If the method is GET or POST fails, render the form again
        form = userLogin()
        return render(request, 'bloodology/login.html', {'form': form})

    else:
        return redirect('home')


#User Logout
def user_logout(request):
    logout(request)
    return redirect('home')


def search(request):
    return render(request,'bloodology/search.html')


def AboutBdonation(request):
    return render(request,'bloodology/question-about-blood.html')