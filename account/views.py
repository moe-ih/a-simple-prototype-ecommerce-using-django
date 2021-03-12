from order.models import Order
from django.shortcuts import redirect, render
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from django.urls import reverse
from django.contrib.auth import authenticate
from django.contrib import messages

from account.models import UserBase
from .forms import RegistrationForm, LoginForm, UserEditForm
from .token import account_activation_token


def user_order(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return orders

@login_required
def dashboard(request):
    orders = user_order(request)

    return render(request,"account/user/dashboard.htm" , context={
        'orders': orders
    })


@login_required
def edit(request):
    old_email = request.user.email
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user,data=request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.email = old_email
            user.save()
            return redirect("account:edit")
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request , "account/user/edit.htm" , {'form' : user_form})


@login_required
def delete_user(request):
    user = UserBase.objects.get(user_name=request.user.user_name)
    user.is_active = False
    user.save()
    logout(request)
    return redirect("account:delete_confrimation")



def delete_confrimation(request):
    return render(request, "account/user/delete_confrimation.htm")

def register_account(request):

    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        register_form = RegistrationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.email = register_form.cleaned_data['email']
            user.user_name = register_form.cleaned_data['user_name']
            
            user.set_password(register_form.cleaned_data['password'])
            user.is_active = False
            user.save()

            # setup for email 

            current_site = get_current_site(request)
            subject = "Activate your Account !!"
            message = render_to_string(
                "account/registration/account_activation_email.htm",{
                    'user'  : user,
                    'domain': current_site.domain,
                    'uuid' :  urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':  account_activation_token.make_token(user)
                })
            user.email_user(subject = subject , message = message)
        
    else:
        register_form = RegistrationForm()
        
    return render(request , "account/registration/register.htm",context={'form': register_form})


def account_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk = uid)
        if user is not None and account_activation_token.check_token(user , token):
            user.is_active = True
            user.save()
            login(request , user)
            
            return redirect("account:dashboard")
            
        else:
            return render(request, "account/registration/invalid_token.htm")

    except:
        return render(request, "account/registration/invalid_token.htm")
        



def custom_login(request):

    if request.user.is_authenticated:
        return redirect("/")

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['user_name']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('account:dashboard'))
            else:
                messages.error(request, 'email or password not correct or your account  not activated !')
                return redirect(reverse('account:login'))
        else:
            pass

    else:
        form = LoginForm()
    return render(request, 'account/login/login.htm', {'form': form})



