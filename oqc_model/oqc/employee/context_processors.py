from django.conf import settings
from .models import *
from authapp.models import *
from django.shortcuts import redirect
from datetime import datetime
import json

def header_context(request):
    excluded_paths = ['/au/login/', '/au/register/', '/au/forgot_password/', '/au/logout/', '/admin/']
    if any(request.path.startswith(prefix) for prefix in excluded_paths):
        return {}
    try:
        username = request.session['username']
    except KeyError:
        next_page = request.original_path
        login_url = '/au/login'
        return redirect(f"{login_url}?next={next_page}" if next_page else login_url)
    employee = Employee.objects.get(username=username)
    notification = Notification.objects.get(employee=employee.username)
    latest_notifications = [notif for notif in notification.notification if not (json.loads(notif)['is_cleared'] or json.loads(notif)['is_read'])]
    latest_notifications = latest_notifications[::-1]
    notif_list = []
    for notif in latest_notifications:
        notify = json.loads(notif)
        created_at = datetime.strptime(notify['created_at'], "%Y-%m-%d %H:%M:%S")
        time_diff = datetime.now() - created_at
        if time_diff.seconds < 60 and time_diff.days == 0:
            notify['created_at_simp'] = "A few seconds ago"
        elif time_diff.seconds < 3600 and time_diff.days == 0:
            notify['created_at_simp'] = f"{time_diff.seconds // 60} min ago"
        elif time_diff.days == 0:
            notify['created_at_simp'] = f"{time_diff.seconds // 3600} hours ago"
        elif time_diff.days == 1:
            notify['created_at_simp'] = "Yesterday"
        else:
            notify['created_at_simp'] = created_at.strftime("%d %b")
        notif_list.append(notify)
    return {
        'latest_notifications': notif_list,
        'notification': notification,
        'employee': employee,
    }