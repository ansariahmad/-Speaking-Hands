from django.contrib import admin
from django.urls import path
from firstapp.views import *
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('view_predictions/<int:id>', admin_view_predictions, name="view_predictions"),
    path('view_login_stats/<int:id>', admin_view_login_stats, name="view_login_stats"),
    path('admin_view/', admin_view, name="admin_view"),
    #path('', TemplateView.as_view(template_name='SignApp.html'), name='home'),
    path('', SignApp, name='SignApp'),
    path('test/', test, name='test'),
    path('index/', index, name='index'),
    # path('video/', video, name='video'), 
    #path('Logoutpage/', Logoutpage, name='logout'),
    path('login/', login_view, name='login'),
    path('logout/', admin_logout, name="admin_logout"),
    path('signup/', signup, name='signup'),
    path('otp_verification/', verify_otp_signup, name="otp_verification"),
    #path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', LogoutView.as_view(next_page=SignApp), name='logout'),
    # path('logout/', logoutPage, name='logout'),
    path('admin_login/', admin_login, name="admin_login"),
    path('updatepass/', updatepass, name='updatepass'),
    path('forget_password_email/', forget_password_email, name="forget_password_email"),
    path('forget_password_otp/', forget_password_otp, name="forget_password_otp"),
    path('forget-update-pass/', forget_updatepass, name="forget_updatepass"),
    path('simple_process_frame/', simple_process_frame, name="simple_process_frame"),
    path('process_frame/', process_frame, name='process_frame'),
    path('process_button/', process_button, name='process_button'),
    path('handle-click/', handle_button_click, name='handle_button_click'),

    path('dashboard_view/', dashboard_view, name='DashBoard'),
    #path('process_video_frame/', process_video_frame, name="process_video_frame")
]

