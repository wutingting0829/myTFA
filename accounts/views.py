from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, UserEditForm, UserProfileForm  
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.http import HttpResponse
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import Profile

# Create your views here.

# @login_required (maybe not needed)
def avatar(request):
   
   if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        avatar = Profile.objects.filter(user=user)
        context = {
            "avatar": avatar,
        }
        return context
   else:
        return {
            'NotLoggedIn': User.objects.none()
        }


@login_required
def profile (request):
    return render(request, 'accounts/profile.html',{'section': 'profile'})  # return the template for this view


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        
        # new enry for profile form
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and user_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)
   
    return render(request,
                  'accounts/update.html',
                  {'user_form': user_form, 'profile_form': profile_form})





@login_required
def delete_user(request):
    if request.method == 'POST':
        user = User.objects.get(username = request.user)
        user.is_active = False
        user.save()
        return redirect('accounts:login')
    return render(request, 'accounts/delete.html')






#  to send an email to the user once who've registered
def accounts_register(request):
    if request.method == 'POST':

         # capture the registion information from this form
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            
            # to set the user is active to false
            user.is_active = True
            user.is_staff = True
            user.save()

            # once the user click the email link then sends them back to our site and to autheticate them
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,

                # the `uid` whcih we pass to the email 
                # in oder to use the user id primary key, we use this url safe base64 encode which basically encodes a byte string to a base64 string for use in urls
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            # return HttpResponse('registered succesfully and activation sent') 
            return redirect('login')
           
    else:
        registerForm = RegistrationForm()
    return render(request, 'registration/register.html', {'form': registerForm})





# to capture the uid decode that and capture the user id 
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # if it successful then wwe can go ahead and set the user activate to ture 
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request,user)
        return redirect('login')
    else:
        return render(request, 'registration/activation_invalid.html')