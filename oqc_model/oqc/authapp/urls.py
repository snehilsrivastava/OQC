# Import necessary modules
from django.contrib import admin # Django admin module
from django.urls import path	 # URL routing
from .views import * # Import views 
from django.conf import settings # Application settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns # Static files serving
from . import views

# Define URL patterns
urlpatterns = [
	path('login/', views.login_page, name='login_page'),
    path('register/', views.register_page, name='register'),
	path('register/send_otp/', views.send_otp, name='send_otp'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('forgot_password/send_otp/', views.forgot_password_send_otp, name='forgot_password_send_otp'),
    path('forgot_password/verify_otp/', views.forgot_password_verify_otp, name='forgot_password_verify_otp'),
    path('forgot_password/update_password/', views.forgot_password_update, name='forgot_password_update'),	
]

# Serve media files if DEBUG is True (development mode)
# if settings.DEBUG:
# 	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# # Serve static files using staticfiles_urlpatterns
# urlpatterns += staticfiles_urlpatterns()
