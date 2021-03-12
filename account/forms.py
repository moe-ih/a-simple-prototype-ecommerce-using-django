from store import models
from django import forms
from .models import UserBase
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm

class RegistrationForm(forms.ModelForm):
    user_name = forms.CharField(
         label="Enter the Username",
         min_length=4, 
         max_length=150,
         help_text="Required",
         widget = forms.TextInput(attrs={'class': "form-control"})
        )
    
    email = forms.CharField(
        label="Email Adress",
        min_length= 4,
        max_length= 300,
        widget=forms.EmailInput(attrs={'class': "form-control"}),
        help_text= "required",
        error_messages= {'required' : 'sorry, you will need an email'},

        )

    password = forms.CharField(label="Password",
     widget=forms.PasswordInput(attrs={'class': "form-control"}),
                               )
    password2 = forms.CharField(label="Repeat Password",
     widget=forms.PasswordInput(attrs={'class': "form-control"}),
                                )


    class Meta:
        model = UserBase
        fields = ('user_name' , 'email')

    def clean_password2(self):
        data_ = self.cleaned_data
        if data_['password'] != data_['password2']:
            raise forms.ValidationError("The Password do not match .")
        return data_['password']


class LoginForm(forms.ModelForm):
    user_name = forms.CharField(label="Email address",widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 
               'placeholder': 'Email', 
               'id': 'login-email'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'login-pwd',
        }
    ))

    class Meta:
        model = UserBase
        fields = ('user_name',)


class UserEditForm(forms.ModelForm):

    email = forms.EmailField(
        label='Account email (can not be changed)', max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}))

    first_name = forms.CharField(
        label='Firstname', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'First name', 'id': 'form-firstname'}))

    user_name = forms.CharField(
        label='Username', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'User name', 'id': 'form-username'}))

    class Meta:
        model = UserBase
        fields = ('email', 'user_name', 'first_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].required = True
        self.fields['email'].required = True
        self.fields['first_name'].required =False


class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label='Account email ', max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'email', 
            'id': 'form-email'}))

    # there is issue here : User enumeration
    #Ref  : https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/03-Identity_Management_Testing/04-Testing_for_Account_Enumeration_and_Guessable_User_Account
    def clean_email(self):
        email = self.cleaned_data['email']
        exist = UserBase.objects.filter(email = email)

        if not exist:
            raise forms.ValidationError("There is No account with that email !")
        
        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))
