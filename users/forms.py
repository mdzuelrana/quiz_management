from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms
from tasks.forms import StyledFormMixin
import re 


from django.contrib.auth.forms import PasswordChangeForm

User = get_user_model()


class ProfileUpdateForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email","bio", "profile_image"]


class CustomPasswordChangeForm(StyledFormMixin,PasswordChangeForm):
    pass

class CustomRegisterForm(StyledFormMixin,forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    confirm_password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')
    
    def cleaned_password(self):
        password=self.cleaned_data.get('password')
        errors=[]
        
        if len(password)<8:
            errors.append('password must be at least 8 character long')
        if not re.search(r'[A-Z]',password):
            errors.append('Password must be uppercase')
        if not re.search(r'[a-z]',password):
            errors.append('Password must be lowercase')
        if not re.search(r'\d',password):
            errors.append('Password must be number')
        if not re.search(r'[@#$%^&+=]',password):
            errors.append('Password must be special character')
        if errors:
            raise forms.ValidationError(errors)
        return password
    
    def clean(self):
        cleaned_data=super().clean()
        password=cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')
        if password and confirm_password and password!=confirm_password:
            raise forms.ValidationError('Password do not match')
        return cleaned_data
    
    def clean_email(self):
        email=self.cleaned_data.get('email')
        email_exists=User.objects.filter(email=email).exists()
        if email_exists:
            raise forms.ValidationError('Email already existed')
        return email
        
        
        

class LoginForm(StyledFormMixin,AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)