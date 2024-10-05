from django.shortcuts import render,HttpResponseRedirect,redirect, get_object_or_404
from . forms import RequestPostForm,UserRegistrationForm,userLogin,VerifyOTPForm,RequestPasswordResetForm,blogPostform
from . models import BloodRequestPost, UserProfile,BlogPost
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . models import User
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password


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

#<============= SignUP ===============>
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

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.utils import timezone
from .models import BloodRequestPost
from .forms import RequestPostForm
from django.contrib.auth.decorators import login_required

# Blood Request Post
@login_required
def AddRequestForm(request):
    now = timezone.now()

    # Delete expired posts where the request time is in the past
    expired_posts = BloodRequestPost.objects.filter(date_time__lt=now)
    expired_posts.delete()

    # Instantiate the form
    form = RequestPostForm()

    if request.method == "POST":
        form = RequestPostForm(request.POST)

        if form.is_valid():
            # Do not call form.save() directly as we need to set user_profile first
            blood_request_post = form.save(commit=False)  # Create an instance but don't save yet
            # Get the logged-in user's profile
            blood_request_post.user_profile = request.user.userprofile
            blood_request_post.save()  # Now save the post with the user_profile

            return HttpResponseRedirect('/')  # Redirect after successful post submission

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
                    messages.error(request, 'Invalid username or password.')
            else:
                messages.error(request, "Invalid username or password.....")

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
    user_instance = User.objects.get(pk=id)  
    user_profile = UserProfile.objects.get(user=user_instance) 

    if request.method == "POST":
        
        fm = UserRegistrationForm(request.POST, request.FILES, instance=user_instance)
        if fm.is_valid():
            user = fm.save(commit=False)  
            
            user_profile.name = fm.cleaned_data['name']
            user_profile.blood_group = fm.cleaned_data['blood_group']
            user_profile.phone_number = fm.cleaned_data['phone_number']
            user_profile.address = fm.cleaned_data['address']
            user_profile.profile_img = fm.cleaned_data.get('profile_img', user_profile.profile_img)  # Keep existing image if none is provided
            user_profile.save()  
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


# Reset Password
def request_password_reset(request):
    if request.method == "POST":
        form = RequestPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                user_profile = user.userprofile
                otp = user_profile.generate_otp()  # Generate and save OTP
                # Send OTP to user's email
                send_mail(
                    'Password Reset OTP',
                    f'Your OTP is {otp}. It will expire in 10 minutes.',
                    'edhimahbub66@gmail.com',  # Replace with your email
                    [user.email],
                    fail_silently=False,
                )
                request.session['reset_user_id'] = user.id  # Store user ID in session for next step
                return redirect('verify_otp')  # Redirect to OTP verification view
            except User.DoesNotExist:
                form.add_error('email', 'No account found with this email.')

    else:
        form = RequestPasswordResetForm()

    return render(request, 'bloodology/request_pass_reset.html', {'form': form})



def verify_otp(request):
    if 'reset_user_id' not in request.session:
        return redirect('request_password_reset')

    user = User.objects.get(id=request.session['reset_user_id'])
    user_profile = user.userprofile
    if request.method == 'POST':
        form = VerifyOTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']

            if user_profile.otp == otp and timezone.now() < user_profile.otp_expiration:
                if new_password == confirm_password:
                    user.password = make_password(new_password)
                    user.save()
                    user_profile.otp = None  # Clear OTP after successful reset
                    user_profile.save()
                    del request.session['reset_user_id']  # Clear session after reset
                    return redirect('login')  # Redirect to login page after successful password reset
                else:
                    form.add_error('confirm_password', 'Passwords do not match.')
            else:
                form.add_error('otp', 'Invalid or expired OTP.')

    else:
        form = VerifyOTPForm()

    return render(request, 'bloodology/verify_otp.html', {'form': form})



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

#blog post
def blog_post(request):
    blog_posts = BlogPost.objects.all().select_related('user_profile').order_by('-blogPostTime')
    return render(request, 'bloodology/blog_list.html', {'blog_posts': blog_posts})

@login_required  # Ensure only logged-in users can access this view
def blogPostFormview(request):
    if request.method == "POST":
        form = blogPostform(request.POST)  # Instantiate form with POST data
        if form.is_valid():  # Check if the form is valid
            blog_post = form.save(commit=False)  # Create a blog post instance without saving it yet
            blog_post.user_profile = request.user.userprofile  # Associate the logged-in user's profile
            blog_post.save()  # Now save the instance
            return redirect('blogapost')  # Redirect to the blog list or another appropriate view
    else:
        form = blogPostform()  # Create an empty form for GET requests

    return render(request, 'bloodology/blogPostForm.html', {'form': form})