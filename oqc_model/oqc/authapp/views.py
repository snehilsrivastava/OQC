from django.shortcuts import render
from django.http import HttpResponse

# Import necessary modules and models
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.hashers import make_password
from employee.models import Employee

# Define a view function for the home page
def home(request):
	return render(request, 'home.html')

# Define custom authenticate function which uses Employee DB
def authenticate(username=None, password=None):
	try:
		user = Employee.objects.using('your_database_name').get(username=username)
	except Employee.DoesNotExist:
		return None

	if user.check_password(password):  # Assuming you're using password hashing
		return user
	return None

# Define a view function for the login page
def login_page(request):
	# Check if the HTTP request method is POST (form submission)
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		
		# Check if a user with the provided username exists
		if not User.objects.filter(username=username).exists():
			# Display an error message if the username does not exist
			messages.error(request, 'Invalid Username')
			return redirect('/login/')
		
		# Authenticate the user with the provided username and password
		user = authenticate(username=username, password=password)
		
		if user is None:
			# Display an error message if authentication fails (invalid password)
			messages.error(request, "Invalid Password")
			return redirect('/au/login/')
		else:
			# Log in the user and redirect to the home page upon successful login
			login(request, user)
			return redirect('/create-test-record/')
	
	# Render the login page template (GET request)
	return render(request, 'login.html')

# Define a view function for the registration page



def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if a user with the provided username already exists
        if Employee.objects.filter(username=username).exists():
            messages.info(request, "Username already taken!")
            return redirect('/au/register/')

        # Create and save the new Employee instance
        new_employee = Employee(
            username=username,
            password=make_password(password)  # Hash the password before saving
        )
        new_employee.save()

        messages.info(request, "Account created Successfully!")
        return HttpResponse("Your details saved successfully!!")

    return render(request, 'register.html')


