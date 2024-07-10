# Import necessary modules
from django.contrib import admin # Django admin module
from django.urls import path	 # URL routing
from .views import * # Import views 
from django.conf import settings # Application settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns # Static files serving
#from . import views

# Define URL patterns
urlpatterns = [
	path('home/', home, name="recipes"),	 # Home page	
	path('login/', login_page, name='login_page'), # Login page 
    path('register/', register_page, name='register'),# Registration page
    path('otp_verification/<str:first_name>/<str:last_name>/<str:username>/<str:password>/', otp_verification, name='otp_verification'),


  
  
]

# Serve media files if DEBUG is True (development mode)
# if settings.DEBUG:
# 	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# # Serve static files using staticfiles_urlpatterns
# urlpatterns += staticfiles_urlpatterns()
