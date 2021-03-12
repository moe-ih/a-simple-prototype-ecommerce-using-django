from django.urls import path
from .views import (register_account, account_activate,dashboard,
                    custom_login,edit,delete_user, delete_confrimation)

from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from .forms import PasswordResetForm, PwdResetConfirmForm

app_name= "account"

urlpatterns = [

    #Auth System
    path("login/", custom_login , name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/account/login/"),name="logout"),
    path("register/", register_account , name="register"),
    path('activate/<slug:uidb64>/<slug:token>/',account_activate, name='activate'),

    # Reset password
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name="account/registration/password_reset_form.htm",
        success_url='password_reset_email_confirm',
        email_template_name='account/registration/password_reset_email.htm',
        form_class=PasswordResetForm), name='pwdreset'),

    path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name='account/registration/password_reset_confirm.htm',
        success_url='password_reset_complete',
        form_class=PwdResetConfirmForm),
        name="password_reset_confirm"),

    path('password_reset/password_reset_email_confirm/',
         TemplateView.as_view(template_name="account/user/reset_status.htm"), name='password_reset_done'),
    path('password_reset_complete/',
         TemplateView.as_view(template_name="account/user/reset_status.htm"), name='password_reset_complete'),
    #profile
    path("dashboard/", dashboard, name="dashboard"),
    path("profile/edit/", edit , name="edit"),
    path("profile/delete_user/", delete_user, name="delete"),
    path("profile/confrim_delete/", delete_confrimation, name="delete_confrimation")


]
