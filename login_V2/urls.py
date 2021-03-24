from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('',views.login_page,name ="login"),
    path('logout/',views.logout_user,name ="logout"),
    path('register/',views.register_page,name = "register"),
    # path('about/',views.about,name = "about"),

    path('reset_password',auth_views.PasswordResetView.as_view(template_name="1.html"), name="reset_password"),
    path('reset_password_sent',auth_views.PasswordResetDoneView.as_view(template_name="login_V2/ForgotPassword/forgot_email_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="login_V2/ForgotPassword/forgot_password.html"), name="password_reset_confirm"),
    path('reset_password_complete',auth_views.PasswordResetCompleteView.as_view(template_name="login_V2/ForgotPassword/password_reset_complete.html"), name="password_reset_complete"),
]
# template_name="login_V2/ForgotPassword/forgot_password.html"