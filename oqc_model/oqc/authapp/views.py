from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login
from .models import *
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime, timedelta
from django.db.models import Q
from random import randint
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.admin.models import LogEntry
import re
import json

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        next_page = request.original_path
        if 'username' in request.session:
            return view_func(request, *args, **kwargs)
        login_url = '/au/login'
        return redirect(f"{login_url}?next={next_page}" if next_page else login_url)
    return wrapper

# Define custom authenticate function which uses Employee DB
def authenticate(username=None, password=None):
    login_user = Employee.objects.get(username=username)
    if check_password(password, login_user.password):
        return login_user
    return None

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not Employee.objects.filter(username=username).exists():
            messages.error(request, 'Invalid Username')
            return redirect('/au/login/')
        
        user = authenticate(username=username, password=password)
        
        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('/au/login/')
        else:
            if not Employee.objects.filter(username=username).first().user_type:
                messages.error(request, 'Account yet to be approved')
                return redirect('/au/login/')
            login(request, user)
            request.session['user_type'] = user.user_type
            request.session['username'] = user.username
            next_page = request.POST.get('next')
            if next_page !='None':
                return redirect(next_page)
            if user.user_type == 'owner':
                return redirect('/dashboard/')
            elif user.user_type == 'legal':
                return redirect('/legal_dashboard/')
            elif user.user_type == 'brand':
                return redirect('/brand_dashboard/')
            else: # Employee
                return redirect('/employee_dashboard/')
    next_page = request.GET.get('next')
    return render(request, 'login.html', {'next': next_page})

def generate_otp(length=6):
    return str(randint(10**(length-1), 10**length -1))

def delete_expired_otps():
    expirations_time = datetime.now() - timedelta(minutes=5)
    OTP.objects.filter(Q(created_at__lt=expirations_time)).delete()
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

def send_otp(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if Employee.objects.filter(username=username).exists():
            messages.warning(request, "Username already exists")
            return JsonResponse({'redirect_url': '/au/login/'})
        valid_domains = ['indkal.com', 'indkaltechno.onmicrosoft.com']
        if username.split('@')[-1] not in valid_domains:
            return JsonResponse({'warning': True, 'message': 'Please enter a valid email address'})
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
        return JsonResponse({'success': True, 'message':'OTP sent successfully'})
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
    elif re.search(r"\s", password):
        return ("Password must not have any whitespace characters")
    else:
        return None
        
def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        pword = request.POST.get('password')
        pword = make_password(pword)
        in_otp = request.POST.get('OTP')
        delete_expired_otps()
        msg = verify_otp(username, in_otp)
        match (msg):
            case 1:
                new_employee = Employee(username=username, first_name=fname, last_name=lname, password=pword)
                new_employee.save()
                new_notification = Notification(employee=new_employee, notification=[])
                new_notification.save()
                messages.success(request, "Account creation request sent.")

                subject = 'New account approval'
                from_email = settings.EMAIL_HOST_USER
                to = ["qmsindkal@gmail.com"]
                text_content = 'This is an important message.'
                html_content = f"""
                <html>
                <body>
                    <p>
                        Hi Protrack,
                        <br><br>You have a new account approval request from {fname} {lname}.
                        <br>Email: {username}<br><br>
                        Click <a href="http://protrackindkal.in/au/admin/" target="_blank">here</a> to go to approval page.
                    </p>
                </body>
                </html>
                """
                msg = EmailMultiAlternatives(subject, text_content, from_email, to)
                msg.attach_alternative(html_content, "text/html")
                msg.send()
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
        send_mail(subject, message, email_from, recipient_list)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

def forgot_password_verify_otp(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        in_otp = request.POST.get('OTP')
        delete_expired_otps()
        msg = verify_otp(username, in_otp)
        match (msg):
            case 1:
                return JsonResponse({'success': True})
            case 2:
                return JsonResponse({'error': True, 'message': 'Invalid or Expired OTP.'})
            case 3:
                return JsonResponse({'error': True, 'message': 'Invalid OTP.'})
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

def forgot_password_update(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        validity = validate_password(password)
        if validity:
            return JsonResponse({'error': True, 'message': validity})
        if password != confirm_password:
            return JsonResponse({'error': True, 'message': 'Passwords do not match'})
        employee = Employee.objects.get(username=username)
        employee.password = make_password(password)
        employee.save()
        messages.success(request, "Password changed successfully!")
        return JsonResponse({'redirect_url': '/au/login/'})
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

@login_required
def admin(request):
    employee = Employee.objects.get(username=request.session['username'])
    if not employee.is_superuser:
        return redirect('/access_denied/')
    icon = employee.first_name[0] + employee.last_name[0]
    approved_users = Employee.objects.filter(user_type__isnull=False)
    approved_users = list(approved_users)[::-1]
    unapproved_users = Employee.objects.filter(user_type__isnull=True)
    unapproved_users = list(unapproved_users)[::-1]
    user_types = ['Product Owner', 'Tester', 'Brand', 'Legal']
    product_types = list(Product_Test_Name_Details.objects.values_list('Product', flat=True))
    context = {
        'username': employee,
        'first_name': employee.first_name,
        'last_name': employee.last_name,
        'icon': icon,
        'approved': approved_users,
        'unapproved': unapproved_users,
        'user_types': user_types,
        'product_types': product_types
    }
    return render(request, 'admin.html', context)

userTypes = {'owner': 'Product Owner', 'employee': 'Tester', 'brand': 'Brand Team', 'legal': 'Legal Team'}

@login_required
def approveUser(request):
    session_user = Employee.objects.get(username=request.session['username'])
    if not session_user.is_superuser:
        return redirect('/access_denied/')
    if request.method == 'POST':
        data = json.loads(request.body)
        user = Employee.objects.get(username=data.get('username'))
        user.user_type = data.get('userType')
        for pt in data.get('productTypes'):
            user.product_type[pt] = True
        user.save()
        # Send email to user
        subject = 'Account approved'
        from_email = settings.EMAIL_HOST_USER
        to = [user.username]

        text_content = ''
        html_content = f"""
        <html>
        <body>
            <p>
                Hi {user.first_name} {user.last_name},<br><br>
                Your account has been approved for {userTypes[user.user_type]} access.<br><br>
                Click <a href="http://protrackindkal.in/au/login" target="_blank">here</a> to go to login page.
            </p>
        </body>
        </html>
        """
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        messages.success(request, 'User approved.')
        return HttpResponse(status=200)

@login_required
def updateUser(request):
    session_user = Employee.objects.get(username=request.session['username'])
    if not session_user.is_superuser:
        return redirect('/access_denied/')
    if request.method == 'POST':
        data = json.loads(request.body)
        user = Employee.objects.get(username=data.get('username'))
        old_user_type = user.user_type
        user.user_type = data.get('userType')
        if data.get('productTypes'):
            for pt in data.get('productTypes'):
                user.product_type[pt] = True
        else:
            for pt in user.product_type.keys():
                user.product_type[pt] = False
        user.save()
        if (old_user_type != user.user_type):
            # Send email to user
            subject = 'Account updated'
            from_email = settings.EMAIL_HOST_USER
            to = [user.username]

            text_content = ''
            html_content = f"""
            <html>
            <body>
                <p>
                    Hi {user.first_name} {user.last_name},<br><br>
                    Your account has been updated for {userTypes[user.user_type]} access.<br><br>
                    Click <a href="http://protrackindkal.in/au/login" target="_blank">here</a> to go to login page.
                </p>
            </body>
            </html>
            """
            msg = EmailMultiAlternatives(subject, text_content, from_email, to)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        messages.success(request, 'Successfully updated user.')
        return HttpResponse(status=200)

@login_required
def removeUser(request, removal_type):
    session_user = Employee.objects.get(username=request.session['username'])
    if not session_user.is_superuser:
        return redirect('/access_denied/')
    if request.method == 'POST':
        data = json.loads(request.body)
        user = Employee.objects.get(username=data.get('username'))
        subject = f'Account {removal_type}'
        from_email = settings.EMAIL_HOST_USER
        to = [user.username]

        text_content = ''
        html_content = f"""
        <html>
        <body>
            <p>
                Hi {user.first_name} {user.last_name},<br><br>
                Your account has been {removal_type}.<br><br>
            </p>
        </body>
        </html>
        """
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        user.delete()
        messages.success(request, 'Successfully removed user.')
        return HttpResponse(status=200)

@login_required
def change_user_type(request, username, user_type):
    user = Employee.objects.get(username=request.session['username'])
    if not user.is_superuser:
        return redirect('/access_denied/')
    change_user = Employee.objects.get(username=username)
    change_user.user_type = user_type
    change_user.save()

    # Send email to user
    subject = 'Account approved'
    from_email = settings.EMAIL_HOST_USER
    to = [change_user.username]

    text_content = ''
    html_content = f"""
    <html>
    <body>
        <p>
            Hi {change_user.first_name} {change_user.last_name},<br><br>
            Your account has been approved for {change_user.user_type} access.<br><br>
            Click <a href="http://protrackindkal.in/au/login" target="_blank">here</a> to go to login page.
        </p>
    </body>
    </html>
    """
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    messages.success(request, 'User type changed successfully.')
    return redirect('/au/admin/')