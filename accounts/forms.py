from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.http import HttpResponse
from pydantic import ValidationError 
from accounts.models import Profile
# need to read the manual to find out er're essentially just overriding some of the existing code that exists in django

# https://docs.djangoproject.com/en/3.0/topics/auth/default/
# https://docs.djangoproject.com/en/3.0/topics/forms/


class PwdChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Old Password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Old Password', 'id': 'form-oldpass'}))
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))



class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New Password', widget=forms.PasswordInput(
            attrs={'class':'form-control mb-3', 'placeholder':'New Password', 'id':'form-newpass'}))
    
    new_password2 = forms.CharField(
        label='Repeat Password', widget=forms.PasswordInput(
            attrs={'class':'form-control mb-3', 'placeholder':'New Password', 'id':'form-newpass'}))


class PwdResetForm( PasswordResetForm):

    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class':'form-control mb-3', 'placeholder':'Email', 'id':'form-email'}))
    
    # to check the user's email if it exists in the database or not.
    def clean_email(self):
        email = self.cleaned_data['email']
        test = User.objects.filter(email=email)

        if not test:
            raise forms.ValidationError(
                'Unfortunatley we can not find that email address'
            )
        return email


class UserLoginForm (AuthenticationForm):

    # to be utilizing widgets , extending and adding our own attributes
    username = forms.CharField(widget=forms.TimeInput(
        attrs={'class': 'form-contorl mb-3', 'placeholder':'Username', 'id': 'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-contorl', 'placeholder':'Password', 'id': 'login-pwd'}))
    


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(
        label='Enter Username', min_length=4, max_length=50, help_text='Required')
    
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={
        'required': 'Sorry, you will need an email'})

    password = forms.CharField(
        label='Password', widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput)

    
    # to validate the passwords are both equal
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',)
    
    # to check the username already exists in the database
    # the username are unique in the system
    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return username
        # return HttpResponse('Username already exists') 
        # return render(request, 'registration/register.html', {'form': registerForm})
    

    #if passwords are not equal, need to type again
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']
    
    
    # to check the email is unique
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, that is already taken')
        return email
    

    # because we imported the model in(class Meta: model=User.....) so we've got access to the model here.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'})


class UserEditForm(forms.ModelForm):
    
    first_name = forms.CharField(
        label='Firstname', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Firstname', 'id': 'form-firstname'}))
    
    last_name = forms.CharField(
        label='Lastname', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Lastname', 'id': 'form-firstname'}))
    
    email = forms.EmailField(
        max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Old Password', 'id': 'form-firstname'}))
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    # the user actual email exists so if the user tries to actually change their email and it already exists with another user.
    # then, we need to capture it right here.
    # def clean_email(self):
    #     email=self.cleaned_data['email']
    #     if User.objects.filter(email=email).exists():
    #         raise forms.ValidationError(
    #             'Please use another Email, that is already taken')
    #     return email
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['last_name'].required = False
        self.fields['email'].required = False

    
# for user profile data form
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']

        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}),
        }