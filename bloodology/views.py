from django.shortcuts import render,HttpResponseRedirect,redirect, get_object_or_404
from . forms import RequestPostForm,UserRegistrationForm,userLogin
from . models import BloodRequestPost, UserProfile
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . models import User


# Create your views here.

def home(request):
    reqPost = BloodRequestPost.objects.all().order_by('-created_at')[:6]
    userProfiles = UserProfile.objects.all()[:4]
    return render(request, 'bloodology/home.html', {'posts': reqPost, 'profiles': userProfiles})


#All Blood request POST
def all_posts(request):
    posts = BloodRequestPost.objects.all().order_by('-created_at') 
    return render(request, 'bloodology/all_blood_request_Post.html', {'posts': posts})

#All Donors Profile
def all_Donors(request):
    query = request.GET.get('blood_group')  # Get the blood group from the search form
    if query:
        posts = UserProfile.objects.filter(blood_group=query)  # Filter by blood group
    else:
        posts = UserProfile.objects.all()  # Show all profiles if no query

    return render(request, 'bloodology/allDonorProfile.html', {'posts': posts, 'query': query})

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
    # Delete expired posts
    now = timezone.now()
    expired_posts = BloodRequestPost.objects.filter(date_time__lt=now)
    print(f"Expired Posts Count Before Deletion: {expired_posts.count()}")  # Debug line

    expired_posts.delete()  # Delete expired posts
    print(f"Expired Posts Deleted. Remaining Count: {BloodRequestPost.objects.count()}")  # Debug line

    form = RequestPostForm()  # Initialize the form at the start
    if request.method == "POST":
        form = RequestPostForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')  # Redirect after successful form submission

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




# <================== delete profile ====================> 

def deleteProfile(request, id):
    if request.method == "POST":
        profile = get_object_or_404(UserProfile, id=id)
        profile.delete()

        logout(request)

        messages.success(request, "Your profile has been deleted successfully.")

        return redirect('home')  
    
    return redirect('home')  
    

# <================== Update/Edit profile ====================> 
def updateProfile(request, id):
    user_instance = User.objects.get(pk=id)  # Get the user instance
    user_profile = UserProfile.objects.get(user=user_instance)  # Get the associated UserProfile

    if request.method == "POST":
        # Initialize the form with POST data and the user instance
        fm = UserRegistrationForm(request.POST, request.FILES, instance=user_instance)
        if fm.is_valid():
            user = fm.save(commit=False)  # Save user but don't commit yet
            # Update UserProfile data
            user_profile.name = fm.cleaned_data['name']
            user_profile.blood_group = fm.cleaned_data['blood_group']
            user_profile.phone_number = fm.cleaned_data['phone_number']
            user_profile.address = fm.cleaned_data['address']
            user_profile.profile_img = fm.cleaned_data.get('profile_img', user_profile.profile_img)  # Keep existing image if none is provided
            user_profile.save()  # Save the UserProfile instance
            user.save()  # Save the User instance
            return redirect('login')  # Redirect to home or a success page after saving
    else:
        # On GET request, load the data into the form
        initial_data = {
            'name': user_profile.name,
            'blood_group': user_profile.blood_group,
            'phone_number': user_profile.phone_number,
            'address': user_profile.address,
            'profile_img': user_profile.profile_img,
        }
        fm = UserRegistrationForm(instance=user_instance)
        fm.fields['name'].initial = initial_data['name']
        fm.fields['blood_group'].initial = initial_data['blood_group']
        fm.fields['phone_number'].initial = initial_data['phone_number']
        fm.fields['address'].initial = initial_data['address']
        # No need to set initial for profile_img as it should be handled in the form directly

    return render(request, 'bloodology/UpdateProfile.html', {'form': fm})

#User Logout
def user_logout(request):
    logout(request)
    return redirect('home')

#Blood Donation Tips
def Blood_Donation_Tips(request):
    return render(request,'bloodology/Blood_Donation_Tips.html')

#Advantage Of Blood Donation
def advantageOfdonation(request):
    return render(request,'bloodology/advantageofblood.html')
#Question About Blood Donation
def AboutBdonation(request):
    return render(request,'bloodology/question-about-blood.html')

#Compatible Blood Donors
def CompatibleBloodDonors(request):
    return render(request,'bloodology/CompatibleBloodDonors.html')

#About Us
def AboutUs(request):
    return render(request,'bloodology/AboutUs.html')