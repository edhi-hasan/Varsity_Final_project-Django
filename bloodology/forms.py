from django import forms 
from .models import BloodRequestPost, UserProfile
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm , UsernameField 
from django.contrib.auth.models import User
from django.utils.translation import gettext,gettext_lazy as _

class RequestPostForm(forms.ModelForm):
    class Meta:
        model = BloodRequestPost
        fields = ['blood_group', 'date_time', 'Disease_name', 'No_of_bag', 'medical_name', 'location', 'phone_number']
        labels = {
            'blood_group': 'Blood Group',
            'date_time': 'Time',
            'Disease_name': 'Disease Name',
            'No_of_bag': 'No of Bag',
            'medical_name': 'Medical Name',
            'location': 'Location',
            'phone_number': 'Phone'
        }
        widgets = {
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'Disease_name': forms.TextInput(attrs={'class': 'form-control'}),
            'No_of_bag': forms.NumberInput(attrs={'class': 'form-control'}),
            'medical_name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'type': 'tel'})
        }

class UserRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=150, label='Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    blood_group = forms.ChoiceField(
        choices=[
            ('A+', 'A+'),
            ('A-', 'A-'),
            ('B+', 'B+'),
            ('B-', 'B-'),
            ('AB+', 'AB+'),
            ('AB-', 'AB-'),
            ('O+', 'O+'),
            ('O-', 'O-'),
        ],
        label='Blood Group',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    phone_number = forms.CharField(max_length=15, label='Phone Number', widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(max_length=250, label='Address', widget=forms.TextInput(attrs={'class': 'form-control'}))
    profile_img = forms.ImageField(required=False, label='Image', widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label='User Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))  # Add email field
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'name', 'blood_group', 'phone_number', 'address', 'profile_img')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']  # Save email to the user
        if commit:
            user.save()  # Save the User instance
            user_profile = UserProfile(
                user=user,
                name=self.cleaned_data['name'],
                blood_group=self.cleaned_data['blood_group'],
                phone_number=self.cleaned_data['phone_number'],
                address=self.cleaned_data['address'],
                profile_img=self.cleaned_data.get('profile_img'),
            )
            user_profile.save()  # Save the UserProfile instance
        return user



class userLogin(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'})
    )