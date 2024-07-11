from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import *
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime, timedelta
from django.db.models import Q
from random import randint
from django.conf import settings
from django.core.mail import send_mail
import re

# Define custom authenticate function which uses Employee DB
def authenticate(username=None, password=None):
    login_user = Employee.objects.get(username=username)
    if check_password(password, login_user.password):
        return login_user
    return None

# Define a view function for the login page
def login_page(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if a user with the provided username exists
        if not Employee.objects.filter(username=username).exists():
            # Display an error message if the username does not exist
            messages.error(request, 'Invalid Username')
            return redirect('/au/login/')
        
        # Authenticate the user with the provided username and password
        user = authenticate(username=username, password=password)
        
        if user is None:
            # Display an error message if authentication fails (invalid password)
            messages.error(request, "Invalid Password")
            return redirect('/au/login/')
        else:
            # Log in the user and redirect to the home page upon successful login
            login(request, user)
            request.session['user_type'] = user.user_type
            request.session['username'] = user.username
            if user.user_type == 'owner':
                return redirect('/dashboard/')
            elif user.user_type == 'legal':
                return redirect('/legal_dashboard/')
            elif user.user_type == 'brand':
                return redirect('/brand_dashboard/')
            else: # Tester
                return redirect('/check/')
    # Render the login page template (GET request)
    return render(request, 'login.html')

def generate_otp(length=6):
    return str(randint(10**(length-1), 10**length -1))

def delete_expired_otps():
    expirations_time = datetime.now() - timedelta(minutes=5)
    OTP.objects.filter(Q(is_verified=True) | Q(created_at__lt=expirations_time)).delete()
    return

def verify_otp(user, otp_code):
    if otp_code:
        try:
            otp_obj = OTP.objects.get(user=user, otp=otp_code, is_verified=False)
            if otp_code == otp_obj.otp:
                otp_obj.is_verified = True
                otp_obj.save()
                return 1
            else:
                return 2
        except OTP.DoesNotExist:
            return 3

# send OTP button
def send_otp(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if a user with the provided username already exists
        if Employee.objects.filter(username=username).exists():
            messages.warning(request, "Username already exists")
            return JsonResponse({'redirect_url': '/au/login/'})
        # Check if the email address is valid
        valid_domains = ['indkal.com', 'indkaltechno.onmicrosoft.com']
        if username.split('@')[-1] not in valid_domains:
            return JsonResponse({'warning': True, 'message': 'Please enter a valid email address'})
        # Check if the password is valid
        validity = validate_password(password)
        if validity:
            return JsonResponse({'warning': True, 'message': validity})

        otp = generate_otp()
        OTP.objects.create(user=username, otp=otp, created_at=datetime.now(), is_verified=False)
        subject = 'OTP'
        message = f'Hi {first_name} {last_name},\nYour OTP is {otp}. It expires in 5 minutes.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [username]
        send_mail(subject, message, email_from, recipient_list)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

def validate_password(password):
    if (len(password)<8):
        return ("Passwords must be at least 8 characters")
    elif not re.search("[a-z]", password):
        return ("Passwords must have at least a lowercase letter")
    elif not re.search("[A-Z]", password):
        return ("Passwords must have at least an uppercase letter")
    elif not re.search("[0-9]", password):
        return ("Passwords must have at least a digit")
    # elif not re.search("[_#@$]" , password):
        # return ("Password must have a special symbol (_, @, #, $)")
    elif re.search("\s" , password):
        return ("Password must not have any whitespace characters")
    else:
        return None
        
# sign up button
def register_page(request):
    if request.method == 'POST':
        # act = request.POST.get('action')
        username = request.POST.get('username')
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        pword = request.POST.get('password')
        pword = make_password(pword)
        in_otp = request.POST.get('OTP')
        new_employee = Employee(username=username, first_name=fname, last_name=lname, password=pword)
        # delete_expired_otps()
        msg = verify_otp(username, in_otp)
        match (msg):
            case 1:
                new_employee.save()
                messages.success(request, "Account created!")
                return redirect('/au/login/')
            case 2:
                messages.error(request, "Invalid or Expired OTP.")
            case 3:
                messages.error(request, "Invalid OTP.")
    return render(request, 'register.html')

def forgot_password(request):
    return render(request, 'forgot_password.html')

def forgot_password_send_otp(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        # Check if a user with the provided username already exists
        if not Employee.objects.filter(username=username).exists():
            return JsonResponse({'error': True, 'message': 'Email doesn\'t exist'})
        employee = Employee.objects.get(username=username)
        first_name = employee.first_name
        last_name = employee.last_name
        otp = generate_otp()
        OTP.objects.create(user=username, otp=otp, created_at=datetime.now(), is_verified=False)
        subject = 'OTP'
        message = f'Hi {first_name} {last_name},\nYour OTP is {otp}. It expires in 5 minutes.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [username]
        # send_mail(subject, message, email_from, recipient_list)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

def forgot_password_verify_otp(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        in_otp = request.POST.get('OTP')
        # delete_expired_otps()
        msg = verify_otp(username, in_otp)
        print(in_otp)
        print(username)
        print(msg)
        match (msg):
            case 1:
                return JsonResponse({'success': True})
            case 2:
                return JsonResponse({'error': True, 'message': 'Invalid or Expired OTP.'})
            case 3:
                return JsonResponse({'error': True, 'message': 'Invalid OTP.'})
    return JsonResponse({'success': False, 'message': 'Invalid request!!!'}, status=400)

def forgot_password_update(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        validity = validate_password(password)
        if validity:
            print(validity)
            return JsonResponse({'error': True, 'message': validity})
        if password != confirm_password:
            return JsonResponse({'error': True, 'message': 'Passwords do not match'})
        employee = Employee.objects.get(username=username)
        employee.password = make_password(password)
        employee.save()
        messages.success(request, "Password changed successfully!")
        return JsonResponse({'redirect_url': '/au/login/'})
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)