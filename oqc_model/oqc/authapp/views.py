from django.http import HttpResponse
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

# Define a view function for the home page
def home(request):
	return render(request, 'home.html')

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
			# request.session['password'] = user.password
			# request.session['last_login'] = user.last_login
			if user.user_type == 'owner':
				return redirect('/dashboard/')
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
def send_otp(request, new_employee):
    if request.method == 'POST':
        # Check if a user with the provided username already exists
        if Employee.objects.filter(username=new_employee.username).exists():
            messages.warning(request, "Email is already registered.")
            return redirect('/au/register/')
        
        # delete_expired_otps()
        otp = generate_otp()
        messages.info(request, f"{otp}")
        OTP.objects.create(user=new_employee.username, otp=otp, created_at=datetime.now(), is_verified=False)
        subject = 'OTP'
        message = f'Hi {new_employee.first_name},\nYour OTP is {otp}. It expires in 5 minutes.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [new_employee.username]
        send_mail(subject, message, email_from, recipient_list)
        messages.success(request, "OTP sent successfully.")
    return

def validate_password(password):
    flag = 0
    while True:
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
# Define a view function for the registration page
def register_page(request):
    if request.method == 'POST':
        act = request.POST.get('action')
        username = request.POST.get('username')
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        pword = request.POST.get('password')
        if username.split('@')[-1] != "indkal.com":
             messages.warning(request, "Please enter a valid email address.")
             return render(request, 'register.html')
        validity = validate_password(pword)
        if validity:
             messages.warning(request, f"{validity}")
             return render(request, 'register.html')
        new_employee = Employee(username=username, first_name=fname, last_name=lname, password=pword)
        in_otp = request.POST.get('OTP')
        if act=='send_otp':
            send_otp(request, new_employee)
            return render(request, 'register.html', context={"employee":new_employee, "password":pword})
        elif act=='sign_up':
            msg = verify_otp(username, in_otp)
            print(msg)
            match (msg):
                case 1:
                    new_employee.save()
                    messages.success(request, "OTP Verified successfully.")
                    messages.success(request, "Account created!")
                    return redirect('/au/login/')
                case 2:
                    messages.error(request, "Invalid or Expired OTP.")
                case 3:
                    messages.error(request, "Invalid OTP.")
        elif act=="otp_resend":
            new_employee = send_otp()
    return render(request, 'register.html')