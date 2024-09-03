from django.conf import settings
from .models import *
from authapp.models import *
from django.shortcuts import redirect
from datetime import datetime

def header_context(request):
    excluded_paths = ['/au/login/', '/au/register/', '/au/forgot_password/', '/au/logout/', '/admin/']
    if any(request.path.startswith(prefix) for prefix in excluded_paths):
        return {}
    try:
        username = request.session['username']
    except KeyError:
        next_page = request.original_path
        login_url = '/au/login'
        print(login_url)
        return redirect(f"{login_url}?next={next_page}" if next_page else login_url)
    employee = Employee.objects.get(username=username)
    notification = Notification.objects.get(employee=employee.username)
    latest_notifications = [notif for notif in notification.notification if not notif['is_cleared']]
    latest_notifications = latest_notifications[::-1]
    for i in range(len(latest_notifications)):
        created_at = datetime.strptime(latest_notifications[i]['created_at'], "%Y-%m-%d %H:%M:%S")
        time_diff = datetime.now() - created_at
        if time_diff.seconds < 60 and time_diff.days == 0:
            latest_notifications[i]['created_at'] = "A few seconds ago"
        elif time_diff.seconds < 3600 and time_diff.days == 0:
            latest_notifications[i]['created_at'] = f"{time_diff.seconds // 60} minutes ago"
        elif time_diff.days == 0:
            latest_notifications[i]['created_at'] = f"{time_diff.seconds // 3600} hours ago"
        elif time_diff.days == 1:
            latest_notifications[i]['created_at'] = f"Yesterday at {created_at.strftime('%I:%M %p')}"
        else:
            latest_notifications[i]['created_at'] = created_at.strftime("%d %b at %I:%M %p")
    return {
        'latest_notifications': latest_notifications,
        'notification': notification,
        'employee': employee,
    }