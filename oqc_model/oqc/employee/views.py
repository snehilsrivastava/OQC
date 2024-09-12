import os
from datetime import date, datetime as dt
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from django.conf import settings
from .forms import *
from .models import *
from .renderers import *
from product.views import *
from authapp.models import Employee, Notification, default_notification
from authapp.views import login_page
import PyPDF2
from io import BytesIO
from django.contrib import messages
from django.db.models import Min, Max, Case, When, DateField
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import json
from django.core.serializers.json import DjangoJSONEncoder

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'username' in request.session:
            return view_func(request, *args, **kwargs)
        next_page = request.original_path
        login_url = '/au/login'
        return redirect(f"{login_url}?next={next_page}" if next_page else login_url)
    return wrapper

@login_required
def access_denied(request):
    user = request.session['username']
    employee = Employee.objects.get(username=user)
    icon = employee.first_name[0] + employee.last_name[0]
    context = {
    }
    return render(request, "access_denied.html", context=context)

@login_required
def custom_404(request):
    context = {}
    return render(request, "404_custom.html", context=context)

def main_page(request):
    try:
        username = request.session['username']
        user = Employee.objects.get(username=username)
        if user.user_type == 'employee':
            return redirect('/employee_dashboard/')
        elif user.user_type == 'owner':
            return redirect('/dashboard/')
        elif user.user_type == 'brand':
            return redirect('/brand_dashboard/')
        elif user.user_type == 'legal':
            return redirect('/legal_dashboard/')
    except KeyError:
        return redirect(login_page)

@login_required
def delete_test_record(request, record_id):
    user = Employee.objects.get(username=request.session['username'])
    if user.user_type != 'employee' and not user.is_superuser:
        return redirect('/access_denied/')
    test_record = get_object_or_404(TestRecord, pk=record_id)
    test_record.delete()
    return redirect('/dashboard/')
    
@login_required
def remark(request, id):
    user = Employee.objects.get(username=request.session['username'])
    if user.user_type != 'employee' and not user.is_superuser:
        return redirect('/access_denied/')
    TestObject = get_object_or_404(TestRecord, pk=id)
    test_name = TestObject.TestName
    model_name = TestObject.ModelName
    serialno = TestObject.SerailNo
    if request.method == 'POST':
        TestObject.employee_remark = request.POST.get('employee-remark')
        TestObject.save()
        return redirect(reverse('view', args=[test_name, model_name, serialno]))
    context = {
        'TestObjectRemark': TestObject,
    }
    return render(request, "remark.html", context)

@login_required
def owner_remark(request, id):
    user = Employee.objects.get(username=request.session['username'])
    if user.user_type != 'owner' and not user.is_superuser:
        return redirect('/access_denied/')
    TestObject = get_object_or_404(TestRecord, pk=id)
    test_name = TestObject.TestName
    model_name = TestObject.ModelName
    serialno = TestObject.SerailNo
    if request.method == 'POST':
        TestObject.owner_remark = request.POST.get('product-owner-remark')
        TestObject.save()
        return redirect(reverse('owner_view', args=[test_name, model_name, serialno]))
    context = {
        'TestObjectRemark': TestObject,
    }
    return render(request, "owner_remark.html", context)

@login_required
def report(request, stage, product, test_name, model_name, serialno):
    user = Employee.objects.get(username=request.session['username'])
    if (user.user_type != 'employee' and user.user_type != 'owner') and not user.is_superuser:
        return redirect('/access_denied/')
    Test_protocol = get_object_or_404(Test_core_detail, TestName=test_name, ProductType=product)
    # product = TestRecord.objects.get(ModelName=model_name, TestName=test_name, SerailNo=serialno).ProductType
    if product == 'AC':
        models = get_object_or_404(AC, ModelName=model_name)
    elif product == 'WM - FATL':
        models = get_object_or_404(WM_FATL, ModelName=model_name)
    test_record = get_object_or_404(TestRecord, ProductType=product, SerailNo=serialno, TestName=test_name, ModelName=model_name, TestStage=stage)
    if request.method == 'POST':
        form = TestRecordForm(request.POST, instance=test_record)  
        if form.is_valid():
            form.save()
            messages.success(request, 'Test record saved successfully.')
        if user.user_type == 'owner':
            return redirect('/dashboard/')
        return redirect('/employee_dashboard/')
    else:
        form = TestRecordForm(instance=test_record)

    context = {
        'testdetail': test_record,
        'TestProtocol': Test_protocol,
        'model': models,
        'form': form,
        'test_name': test_name,
        'model_name': model_name,
        'serialno': serialno
    }
    return render(request, "report.html", context)

def set_status(request, id):
    user = Employee.objects.get(username=request.session['username'])
    if user.user_type != 'employee' and not user.is_superuser:
        return redirect('/access_denied/')
    test_record = TestRecord.objects.get(id=id)
    test_record.status = "Waiting"
    test_record.test_end_date = date.today()
    test_record.test_date = date.today()
    test_record.save()

    product = test_record.ProductType
    owner_employees = Employee.objects.filter(user_type='owner')
    for employee in owner_employees:
        if employee.product_type[product]:
            notification = Notification.objects.get(employee=employee)
            notification_dict = default_notification()
            notification_dict["from"] = f"{user.first_name} {user.last_name}"
            notification_dict["display_content"] = f"{user.first_name} {user.last_name} sent a report for approval."
            notification_dict["display_full_content"] = f"Sent a report for product: {test_record.ProductType}, model: {test_record.ModelName}, stage: {test_record.TestStage} and test name: {test_record.TestName}."
            notification_dict["metadata"]["product"] = test_record.ProductType
            notification_dict["metadata"]["model"] = test_record.ModelName
            notification_dict["metadata"]["stage"] = test_record.TestStage
            notification_dict["metadata"]["test"] = test_record.TestName
            notification_dict["metadata"]["serialno"] = test_record.SerailNo
            notification_dict["action"] = "sent-1"
            notif_dict = json.dumps(notification_dict)
            notification.notification.append(notif_dict)
            notification.unread_count += 1
            notification.save()
    messages.success(request, 'Record sent to PO for approval.')
    return redirect('/employee_dashboard/')

from django.contrib.auth import logout as auth_logout

@login_required
def logout(request):
    if request.method == "POST":
        auth_logout(request)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@login_required
def edit(request, stage, product, test_name, model_name, serialno):
    user = Employee.objects.get(username=request.session['username'])
    if user.user_type != 'employee' and not user.is_superuser:
        return redirect('/access_denied/')
    Test_protocol = get_object_or_404(Test_core_detail, TestName=test_name, ProductType=product)
    # product = TestRecord.objects.get(ModelName=model_name, TestName=test_name, SerailNo=serialno, TestStage=stage).ProductType
    if product == 'AC':
        models = get_object_or_404(AC, ModelName=model_name)
    elif product == 'WM - FATL':
        models = get_object_or_404(WM_FATL, ModelName=model_name)
    test_record = get_object_or_404(TestRecord, ProductType=product, TestStage=stage, SerailNo=serialno, TestName=test_name, ModelName=model_name)
    if request.method == 'POST':
        test_record.test_end_date = date.today()
        test_record.test_date = date.today()
        test_record.save()
        form = TestRecordForm(request.POST, instance=test_record)  
        if form.is_valid():
            form.save()
            messages.success(request, 'Test record updated.')
        else:
            messages.error(request, 'Failed to update test record.')
        if user.user_type == 'owner':
            return redirect('/dashboard/')
        return redirect('/employee_dashboard/')
    else:
        form = TestRecordForm(instance=test_record)
    test_record.additional_details = test_record.additional_details.strip()
    context = {
        'testdetail': test_record,
        'TestProtocol': Test_protocol,
        'model': models,
        'form': form,
        'test_name': test_name,
        'model_name': model_name,
        'serialno': serialno,
        'product': product,
        'stage': stage
    }
    return render(request, "report.html", context)

@login_required
def view_pdf(request, stage, product, test_name, model_name, serialno):
    Test_protocol = get_object_or_404(Test_core_detail, TestName=test_name, ProductType=product)
    # product = TestRecord.objects.get(ModelName=model_name, TestName=test_name, SerailNo=serialno, TestStage=stage).ProductType
    if product == 'AC':
        models = get_object_or_404(AC, ModelName=model_name)
    elif product == 'WM - FATL':
        models = get_object_or_404(WM_FATL, ModelName=model_name)
    test_record = get_object_or_404(TestRecord, SerailNo=serialno, TestStage=stage, ModelName=model_name, ProductType=product, TestName=test_name)
    context = {
        'TestProtocol': Test_protocol,
        'model': models,
        'test': test_record,
        'testdetail': test_record,
    }
    return render(request, "view_pdf.html", context)

@login_required
def pdf_model_stage(request,model_name,test_stage):
    if request.method == 'GET':
        selected_test_records = TestRecord.objects.filter(ModelName=model_name, TestStage=test_stage)
        selected_test_records = selected_test_records.exclude(L_status='Not Sent')
        if not selected_test_records.exists():
            raise Http404("No test records found")
        pdf_list = []
        cumul_page_count, cumul_page_count_list = 3, []
        test_name_list = []
        for i, test_record in enumerate(selected_test_records, start=1):
            model_name = test_record.ModelName
            test_name = test_record.TestName
            Test_protocol = get_object_or_404(Test_core_detail, TestName=test_name)
            product = TestRecord.objects.filter(ModelName=model_name, TestName=test_name).first().ProductType
            if product == 'AC':
                models = get_object_or_404(AC, ModelName=model_name)
            elif product == 'WM - FATL':
                models = get_object_or_404(WM_FATL, ModelName=model_name)
            context = {
                'test': test_record,
                'model': models,
                'TestProtocol': Test_protocol,
                'testdetail': test_record,
            }
            test_name_list.append(test_name)
            cumul_page_count_list.append(cumul_page_count)
            pdf_content, page_count = render_to_pdf('view_pdf.html', context, request)
            pdf_list.append(BytesIO(pdf_content))
            cumul_page_count += page_count

        if len(pdf_list) > 1:  # No cover page or table of contents for one test
            test_record = selected_test_records[0] # assuming all records are for same model
            model_name = test_record.ModelName
            MNF_detail = get_object_or_404(Model_MNF_detail, Indkal_model_no=model_name)
            start_date = selected_test_records.aggregate(
                min_date=Min(Case(
                    When(verification=True, then='test_date'),
                    default='test_start_date',
                    output_field=DateField()
                ))
            )['min_date']
            end_date = selected_test_records.aggregate(
                max_date=Max(Case(
                    When(verification=True, then='test_date'),
                    default='test_end_date',
                    output_field=DateField()
                ))
            )['max_date']
            cover_context = {
                'MNF_detail': MNF_detail,
                'start_date': start_date,
                'end_date': end_date,
                'issue_date': date.today(),
            }
            pdf_list.insert(0, BytesIO(render_cover_to_pdf('pdf_cover.html', cover_context, request)))
            context_list = [[a, b] for a, b in zip(test_name_list, cumul_page_count_list)]
            pdf_list.insert(1, BytesIO(render_contents_to_pdf('pdf_contents.html', {'list': context_list}, request)))
        merged_pdf = merge_pdfs(pdf_list)
        response = HttpResponse(merged_pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{test_record.ModelName}_{test_record.TestStage}.pdf"'
        return response
    return HttpResponse("Invalid request method.", status=405)

def merge_pdfs(pdf_list):
    merger = PyPDF2.PdfMerger()
    for pdf in pdf_list:
        pdf.seek(0)
        merger.append(pdf)

    merged_pdf_io = BytesIO()
    merger.write(merged_pdf_io)
    merged_pdf_io.seek(0)
    return merged_pdf_io

@login_required
def handle_selected_tests(request):
    user = Employee.objects.get(username=request.session['username'])
    if user.user_type not in ['owner', 'brand', 'legal'] and not user.is_superuser:
        return redirect('/access_denied/')
    if request.method == 'POST':
        selected_test_ids = request.POST.getlist('selected_tests')
        action = request.POST.get('action')
        selected_test_records = TestRecord.objects.filter(pk__in=selected_test_ids)
        if action == 'generate_pdf':
            if not selected_test_records.exists():
                messages.error(request, 'No test records selected')
                if user.user_type=='owner':      
                    return redirect('/dashboard/')
                elif user.user_type=='legal':      
                    return redirect('/legal_dashboard/')
                elif user.user_type=='brand':      
                    return redirect('/brand_dashboard/')
            pdf_list = []
            cumul_page_count, cumul_page_count_list = 3, []
            test_name_list = []
            for i, test_record in enumerate(selected_test_records, start=1):
                model_name = test_record.ModelName
                test_name = test_record.TestName
                product = test_record.ProductType
                Test_protocol = get_object_or_404(Test_core_detail, TestName=test_name, ProductType=product)
                if product == 'AC':
                    models = get_object_or_404(AC, ModelName=model_name)
                elif product == 'WM - FATL':
                    models = get_object_or_404(WM_FATL, ModelName=model_name)
                context = {
                'test': test_record,
                'model': models,
                'TestProtocol': Test_protocol,
                'testdetail': test_record,
                }
                test_name_list.append(test_name)
                cumul_page_count_list.append(cumul_page_count)
                pdf_content, page_count = render_to_pdf('view_pdf.html', context, request)
                pdf_list.append(BytesIO(pdf_content))
                cumul_page_count += page_count

            if len(pdf_list) > 1:  # No cover page or table of contents for one test
                test_record = selected_test_records[0] # assuming all records are for same model
                model_name = test_record.ModelName
                MNF_detail = get_object_or_404(Model_MNF_detail, Indkal_model_no=model_name)
                start_date = selected_test_records.aggregate(
                    min_date=Min(Case(
                        When(verification=True, then='test_date'),
                        default='test_start_date',
                        output_field=DateField()
                    ))
                )['min_date']
                end_date = selected_test_records.aggregate(
                    max_date=Max(Case(
                        When(verification=True, then='test_date'),
                        default='test_end_date',
                        output_field=DateField()
                    ))
                )['max_date']
                cover_context = {
                    'MNF_detail': MNF_detail,
                    'start_date': start_date,
                    'end_date': end_date,
                    'issue_date': date.today(),
                }
                pdf_list.insert(0, BytesIO(render_cover_to_pdf('pdf_cover.html', cover_context, request)))
                context_list = [[a, b] for a, b in zip(test_name_list, cumul_page_count_list)]
                pdf_list.insert(1, BytesIO(render_contents_to_pdf('pdf_contents.html', {'list': context_list}, request)))
            merged_pdf = merge_pdfs(pdf_list)
            response = HttpResponse(merged_pdf, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{test_record.ModelName}_{test_record.TestStage}.pdf"'
            return response

        elif action == 'send_brand':
            if not selected_test_records.exists():
                messages.error(request, 'No test records selected')
                return redirect('/dashboard/')
            count = 0
            for test_record in selected_test_records:
                if test_record.B_status != "Approved" and test_record.status == "Approved":
                    count += 1
                    test_record.B_status = "Waiting"
                    test_record.owner_name = user.first_name + " " + user.last_name
                    test_record.save()
            if count == 0:
                messages.warning(request, 'No tests sent to Brand Team.')
            else:
                brand_employees = Employee.objects.filter(user_type='brand')
                for employee in brand_employees:
                    notification = Notification.objects.get(employee=employee)
                    notification_dict = default_notification()
                    test_record = selected_test_records[0]
                    notification_dict["metadata"] = {
                        "product": test_record.ProductType,
                        "model": test_record.ModelName,
                        "stage": test_record.TestStage,
                    }
                    if count == 1:
                        notification_dict["display_content"] = f"{user.first_name} {user.last_name} sent a report for approval."
                        notification_dict["display_full_content"] = f"Sent a report for product: {test_record.ProductType}, model: {test_record.ModelName}, stage: {test_record.TestStage} and test name: {test_record.TestName}."
                        notification_dict["metadata"]["test"] = test_record.TestName
                        notification_dict["metadata"]["serialno"] = test_record.SerailNo
                        notification_dict["action"] = "sent-1"
                    else:
                        notification_dict["display_content"] = f"{user.first_name} {user.last_name} sent {count} reports for approval."
                        notification_dict["display_full_content"] = f"Sent {count} reports for product: {test_record.ProductType}, model: {test_record.ModelName} and stage: {test_record.TestStage}."
                        notification_dict["action"] = "sent"
                    notification_dict["from"] = user.first_name + " " + user.last_name
                    notif_dict = json.dumps(notification_dict)
                    notification.notification.append(notif_dict)
                    notification.unread_count += 1
                    notification.save()
                messages.success(request, 'Sent to Brand Team for approval.')

        elif action == 'send_legal':
            if not selected_test_records.exists():
                messages.error(request, 'No test records selected')
                return redirect('/dashboard/')
            count = 0
            for test_record in selected_test_records:
                if test_record.L_status != "Approved" and test_record.status == "Approved":
                    count += 1
                    test_record.L_status = "Waiting"
                    test_record.owner_name = user.first_name + " " + user.last_name
                    test_record.save()
            if count == 0:
                messages.warning(request, 'No tests sent to Legal Team.')
            else:
                legal_employees = Employee.objects.filter(user_type='legal')
                for employee in legal_employees:
                    notification = Notification.objects.get(employee=employee)
                    notification_dict = default_notification()
                    test_record = selected_test_records[0]
                    notification_dict["metadata"] = {
                        "product": test_record.ProductType,
                        "model": test_record.ModelName,
                        "stage": test_record.TestStage,
                    }
                    if count == 1:
                        notification_dict["display_content"] = f"{user.first_name} {user.last_name} sent a report for approval."
                        notification_dict["display_full_content"] = f"Sent a report for product: {test_record.ProductType}, model: {test_record.ModelName}, stage: {test_record.TestStage} and test name: {test_record.TestName}."
                        notification_dict["metadata"]["test"] = test_record.TestName
                        notification_dict["metadata"]["serialno"] = test_record.SerailNo
                        notification_dict["action"] = "sent-1"
                    else:
                        notification_dict["display_content"] = f"{user.first_name} {user.last_name} sent {count} reports for approval."
                        notification_dict["display_full_content"] = f"Sent {count} reports for product: {test_record.ProductType}, model: {test_record.ModelName} and stage: {test_record.TestStage}."
                        notification_dict["action"] = "sent"
                    notification_dict["from"] = user.first_name + " " + user.last_name
                    notif_dict = json.dumps(notification_dict)
                    notification.notification.append(notif_dict)
                    notification.unread_count += 1
                    notification.save()
                messages.success(request, 'Sent to Legal Team for approval.')

    return redirect('/dashboard/')

@login_required
def view(request, stage, product, test_name, model_name, serialno):
    user = Employee.objects.get(username=request.session['username'])
    if user.user_type != 'employee' and not user.is_superuser:
        return redirect('/access_denied/')
    Test_protocol = get_object_or_404(Test_core_detail, TestName=test_name, ProductType=product)
    # product = TestRecord.objects.get(ModelName=model_name, TestName=test_name, SerailNo=serialno, TestStage=stage).ProductType
    if product == 'AC':
        models = get_object_or_404(AC, ModelName=model_name)
    elif product == 'WM - FATL':
        models = get_object_or_404(WM_FATL, ModelName=model_name)
    test_record = get_object_or_404(TestRecord, ProductType=product, ModelName=model_name, SerailNo=serialno , TestName=test_name, TestStage=stage)
    page_break = '''<hr style="border-top: solid black; width: 100%;">'''
    soup = BeautifulSoup(test_record.additional_details, 'html.parser')
    paragraphs = soup.find_all('p')
    page_break_paragraphs = [p for p in paragraphs if p.text.strip().lower() == "pagebreak"]
    for p in page_break_paragraphs:
        p.string = ""
        p.append(BeautifulSoup(page_break, 'html.parser'))
    test_record.additional_details = str(soup)
    context = {
        'TestProtocol': Test_protocol,
        'model': models,
        'test': test_record,
        'testdetail': test_record,
    }
    return render(request, "view_test_record.html", context)

@login_required
def owner_view(request, stage, product, test_name, model_name, serialno):
    user = Employee.objects.get(username=request.session['username'])
    if user.user_type != 'owner' and not user.is_superuser:
        return redirect('/access_denied/')
    Test_protocol = get_object_or_404(Test_core_detail, TestName=test_name, ProductType=product)
    product = TestRecord.objects.get(ModelName=model_name, TestName=test_name, SerailNo=serialno, TestStage=stage).ProductType
    if product == 'AC':
        models = get_object_or_404(AC, ModelName=model_name)
    elif product == 'WM - FATL':
        models = get_object_or_404(WM_FATL, ModelName=model_name)
    test_record = get_object_or_404(TestRecord, ProductType=product, SerailNo=serialno, ModelName=model_name, TestName=test_name, TestStage=stage)
    page_break = '''<hr style="border-top: solid black; width: 100%;">'''
    soup = BeautifulSoup(test_record.additional_details, 'html.parser')
    paragraphs = soup.find_all('p')
    page_break_paragraphs = [p for p in paragraphs if p.text.strip().lower() == "pagebreak"]
    for p in page_break_paragraphs:
        p.string = ""
        p.append(BeautifulSoup(page_break, 'html.parser'))
    test_record.additional_details = str(soup)
    context = {
        'testdetail': test_record,
        'TestProtocol': Test_protocol,
        'model': models,
        'test': test_record,
        'test_name': test_name,
        'model_name': model_name,
        'serialno': serialno
    }
    return render(request, "owner_view.html", context)

@login_required
def change_status(request, test_id, status):
    user = Employee.objects.get(username=request.session['username'])
    if user.user_type != 'owner' and not user.is_superuser:
        return redirect('/access_denied/')
    test = get_object_or_404(TestRecord, id=test_id)
    old_status = test.status
    if status == 1:
        test.status = 'Waiting'
    elif status == 2:
        test.status = 'Approved'
    else:
        test.status = 'Rejected'
    test.save()
    if status != 1 and test.status != old_status:
        tester_employees = Employee.objects.filter(user_type="employee")
        for employee in tester_employees:
            if employee.product_type[test.ProductType]:
                notification = Notification.objects.get(employee_id=employee)
                notification_dict = default_notification()
                notification_dict["from"] = f"{user.first_name} {user.last_name}"
                if status == 2:
                    notification_dict["action"] = "approved"
                    notification_dict["display_content"] = f"{user.first_name} {user.last_name} approved a report"
                    notification_dict["display_full_content"] = f"Approved a report for model: {test.ModelName}, stage: {test.TestStage} and test name: {test.TestName}"
                elif status == 3:
                    notification_dict["action"] = "rejected"
                    notification_dict["display_content"] = f"{user.first_name} {user.last_name} rejected a report"
                    notification_dict["display_full_content"] = f"Rejected a report for model: {test.ModelName}, stage: {test.TestStage} and test name: {test.TestName}"
                notification_dict["metadata"]["product"] = test.ProductType
                notification_dict["metadata"]["model"] = test.ModelName
                notification_dict["metadata"]["stage"] = test.TestStage
                notification_dict["metadata"]["test"] = test.TestName
                notification_dict["metadata"]["serialno"] = test.SerailNo
                notif_dict = json.dumps(notification_dict)
                notification.notification.append(notif_dict)
                notification.unread_count += 1
                notification.save()
    test_name = test.TestName
    model_name = test.ModelName
    serialno = test.SerailNo
    return redirect('owner_view', test_name=test_name, model_name=model_name, serialno=serialno)

def send_change_status_notification(request, test, from_func):
    owner_employees = Employee.objects.filter(user_type="owner")
    user = Employee.objects.get(username=request.session['username'])
    for owner in owner_employees:
        if owner.product_type[test.ProductType]:
            notification = Notification.objects.get(employee_id=owner)
            notification_dict = default_notification()
            notification_dict["from"] = f"{user.first_name} {user.last_name}"
            if from_func == "legal":
                if test.L_status == "Approved":
                    notification_dict["action"] = "approved"
                    notification_dict["display_content"] = f"{user.first_name} {user.last_name} (legal team) approved a report"
                    notification_dict["display_full_content"] = f"Legal Team approved a report for model: {test.ModelName}, stage: {test.TestStage} and test name: {test.TestName}"
                elif test.L_status == "Rejected":
                    notification_dict["action"] = "rejected"
                    notification_dict["display_content"] = f"{user.first_name} {user.last_name} (legal team) rejected a report"
                    notification_dict["display_full_content"] = f"Legal Team rejected a report for model: {test.ModelName}, stage: {test.TestStage} and test name: {test.TestName}"
            elif from_func == "brand":
                if test.B_status == "Approved":
                    notification_dict["action"] = "approved"
                    notification_dict["display_content"] = f"{user.first_name} {user.last_name} (brand team) approved a report"
                    notification_dict["display_full_content"] = f"Brand Team approved a report for model: {test.ModelName}, stage: {test.TestStage} and test name: {test.TestName}"
                elif test.B_status == "Rejected":
                    notification_dict["action"] = "rejected"
                    notification_dict["display_content"] = f"{user.first_name} {user.last_name} (brand team) rejected a report"
                    notification_dict["display_full_content"] = f"Brand Team rejected a report for model: {test.ModelName}, stage: {test.TestStage} and test name: {test.TestName}"
            notification_dict["metadata"]["product"] = test.ProductType
            notification_dict["metadata"]["model"] = test.ModelName
            notification_dict["metadata"]["stage"] = test.TestStage
            notification_dict["metadata"]["test"] = test.TestName
            notification_dict["metadata"]["serialno"] = test.SerailNo
            notif_dict = json.dumps(notification_dict)
            notification.notification.append(notif_dict)
            notification.unread_count += 1
            notification.save()

@login_required
def change_status_legal(request, test_id, status):
    user = Employee.objects.get(username=request.session['username'])
    if user.user_type != 'legal' and not user.is_superuser:
        return redirect('/access_denied/')
    test = get_object_or_404(TestRecord, id=test_id)
    old_status = test.L_status
    if status == 1:
        test.L_status = "Waiting"
    elif status == 2:
        test.L_status = "Approved"
    else:
        test.L_status = "Rejected"
    test.save()
    if status != 1 and test.L_status != old_status:
        send_change_status_notification(request, test, "legal")
    test_name = test.TestName
    model_name = test.ModelName
    serialno = test.SerailNo
    return redirect('legal_view', test_name=test_name, model_name=model_name, serialno=serialno)

@login_required
def change_status_brand(request, test_id, status):
    user = Employee.objects.get(username=request.session['username'])
    if user.user_type != 'brand' and not user.is_superuser:
        return redirect('/access_denied/')
    test = get_object_or_404(TestRecord, id=test_id)
    old_status = test.B_status
    if status == 1:
        test.B_status = "Waiting"
    elif status == 2:
        test.B_status = "Approved"
    else:
        test.B_status = "Rejected"
    test.save()
    if status != 1 and test.B_status != old_status:
        send_change_status_notification(request, test, "brand")
    test_name = test.TestName
    model_name = test.ModelName
    serialno = test.SerailNo
    return redirect('brand_view', test_name=test_name, model_name=model_name, serialno=serialno)

def summary():
    ret = []
    status_colors = {"Uploading": "Maroon", "Uploaded": "#989800", "Completed": "Green"}
    PType = Product_List.objects.values('Product')
    ProductType = [_['Product'] for _ in PType]
    for P in ProductType:
        Models = Model_Test_Name_Details.objects.filter(Product=P)
        for M in Models:
            stage_wise = {"DVT": [], "PP": [], "MP": []}
            curr_stage = "DVT"

            today = dt.now()
            for S in ["DVT", "PP", "MP"][::-1]:
                if M.Time_Line[S][0]:
                    curr_stage = S if dt.strptime(M.Time_Line[S][0], "%d/%m/%Y") < today else curr_stage

            for S in ["DVT", "PP", "MP"]:
                total_count = M.Test_Count[S]
                end_date = M.Time_Line[S][1]
                if end_date:
                    end_date = dt.strptime(end_date, "%d/%m/%Y")
                    end_date_color = "lime" if (end_date > dt.now() and curr_stage == S) else "#ff4d4d" if (end_date < dt.now() and curr_stage == S) else "white"
                else:
                    end_date_color = "white"
                TestRecords = TestRecord.objects.filter(ProductType=P, ModelName=M.Model_Name.Indkal_model_no, TestStage=S)
                PS, BS, LS = "Completed", "Completed", "Completed"
                PO_Approved, PO_Uploaded, PO_Uploading = 0, 0, 0
                BT_Approved, BT_Uploaded, BT_Uploading = 0, 0, 0
                LT_Approved, LT_Uploaded, LT_Uploading = 0, 0, 0
                for T in TestRecords:
                    POS = T.status
                    BTS = T.B_status
                    LTS = T.L_status
                    if POS=="Approved":
                        PO_Approved += 1
                    elif POS=="Not Sent":
                        PO_Uploading += 1
                    elif POS=="Waiting":
                        PO_Uploaded += 1
                    if BTS=="Approved":
                        BT_Approved += 1
                    elif BTS=="Not Sent":
                        BT_Uploading += 1
                    elif BTS=="Waiting":
                        BT_Uploaded += 1
                    if LTS=="Approved":
                        LT_Approved += 1
                    elif LTS=="Not Sent":
                        LT_Uploading += 1
                    elif LTS=="Waiting":
                        LT_Uploaded += 1
                    if POS=="Waiting" and PS=="Completed":
                        PS = "Uploaded"
                    elif POS=="Not Sent" and (PS=="Completed" or PS=="Uploaded"):
                        PS = "Uploading"
                    if BTS=="Waiting" and BS=="Completed":
                        BS = "Uploaded"
                    elif BTS=="Not Sent" and (BS=="Completed" or BS=="Uploaded"):
                        BS = "Uploading"
                    if LTS=="Waiting" and LS=="Completed":
                        LS = "Uploaded"
                    elif LTS=="Not Sent" and (LS=="Completed" or LS=="Uploaded"):
                        LS = "Uploading"
                combined_count = {"PO": [total_count, PO_Approved, PO_Uploaded, PO_Uploading], "BT": [total_count, BT_Approved, BT_Uploaded, BT_Uploading], "LT": [total_count, LT_Approved, LT_Uploaded, LT_Uploading]}
                status = [status_colors[PS], status_colors[BS], status_colors[LS]]
                stage_wise[S] = {"Count": combined_count, "Status": status, "TimeLine": M.Time_Line[S], "EndDateColor": end_date_color}
            ret.append({"Meta": [P, M.Model_Name.Indkal_model_no, curr_stage], "Stage_wise": stage_wise})
    return ret

@login_required
def dashboard(request):
    username = request.session['username']
    user = Employee.objects.get(username=username)
    if user.user_type != 'owner' and not user.is_superuser:
        return redirect('/access_denied/')
    test_name = request.GET.get('test_name', '')
    test_stage = request.GET.get('test_stage', '')
    product = request.GET.get('product','')
    model_name = request.GET.get('model_name', '')
    serial_number = request.GET.get('serial_number', '')
    status = request.GET.get('status', '')
    L_status = request.GET.get('L_status','')
    B_status = request.GET.get('B_status','')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    status_color = {"Not Sent": "#cfcfcf", "Waiting": "Yellow", "Approved": "#5AA33F", "Rejected": "Red"}
    role_letter = {"T": "Test Inspector", "L": "Legal Team", "B": "Brand Team"}

    user_ProdType = [k for k in user.product_type if user.product_type[k]]
    if len(user_ProdType) == 1:
        product = user_ProdType[0]
    completed_tests = TestRecord.objects.all()
    completed_tests = completed_tests.filter(ProductType__in=user_ProdType)
    if test_name:
        completed_tests = completed_tests.filter(TestName=test_name)
    if product:
        completed_tests = completed_tests.filter(ProductType=product)
    if test_stage:
        completed_tests = completed_tests.filter(TestStage=test_stage)
    if model_name:
        completed_tests = completed_tests.filter(ModelName=model_name)
    if serial_number:
        completed_tests = completed_tests.filter(SerailNo=serial_number)
    if status:
        completed_tests = completed_tests.filter(status=status)
    if L_status:
        completed_tests = completed_tests.filter(L_status= L_status)
    if B_status:
        completed_tests = completed_tests.filter(B_status= B_status)
    if start_date:
        completed_tests = completed_tests.filter(test_date__gte=start_date)
    if end_date:
        completed_tests = completed_tests.filter(test_date__lte=end_date)
    tests = completed_tests.values('ProductType', 'ModelName').distinct()
    completed_tests = completed_tests.order_by('-test_end_date')
    models_list = json.dumps(list(Model_Test_Name_Details.objects.all().values()))
    test = json.dumps(list(TestRecord.objects.all().values()), cls=DjangoJSONEncoder)
    summary_data = summary()
    summary_ = []
    for sum in summary_data:
        if sum['Meta'][0] in user_ProdType:
            summary_.append(sum)
    context = {
        'test': test,
        'tests': tests,
        'all_tests': completed_tests,
        'test_name': test_name,
        'test_stage': test_stage,
        'model_name': model_name,
        'serial_number': serial_number,
        'status': status,
        'L_status' : L_status,
        'B_status' : B_status,
        'product':product,
        'start_date': start_date,
        'end_date': end_date,
        'models_list': models_list,
        'status_color' : status_color,
        'role_letter': role_letter,
        'summary_data': summary_,
        'userProductTypes': user_ProdType
    }
    return render(request, 'dashboard_PO.html', context)

@login_required
def employee_dashboard(request):
    username = request.session['username']
    user = Employee.objects.get(username=username)
    if user.user_type != 'employee' and not user.is_superuser:
        return redirect('/access_denied/')
    test_name = request.GET.get('test_name', '')
    test_stage = request.GET.get('test_stage', '')
    product = request.GET.get('product','')
    model_name = request.GET.get('model_name', '')
    serial_number = request.GET.get('serial_number', '')
    status = request.GET.get('status', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    
    user_ProdType = [k for k in user.product_type if user.product_type[k]]
    completed_tests = TestRecord.objects.filter(ProductType__in=user_ProdType)

    if test_name:
        completed_tests = completed_tests.filter(TestName=test_name)
    if product:
        completed_tests = completed_tests.filter(ProductType=product)
    if test_stage:
        completed_tests = completed_tests.filter(TestStage=test_stage)
    if model_name:
        completed_tests = completed_tests.filter(ModelName=model_name)
    if serial_number:
        completed_tests = completed_tests.filter(SerailNo=serial_number)
    if status:
        completed_tests = completed_tests.filter(status=status)
    if start_date:
        completed_tests = completed_tests.filter(test_date__gte=start_date)
    if end_date:
        completed_tests = completed_tests.filter(test_date__lte=end_date)
    completed_tests = completed_tests.order_by('-test_end_date')
    tv_models = list(TV.objects.values_list('ModelName', flat=True))
    ac_models = list(AC.objects.values_list('ModelName', flat=True))
    phone_models = list(Phone.objects.values_list('ModelName', flat=True))
    washing_machine_models = list(WM_FATL.objects.values_list('ModelName', flat=True))
    test = json.dumps(list(TestRecord.objects.all().values()), cls=DjangoJSONEncoder)
    context = {
        'test': test,
        'completed_tests': completed_tests,
        'test_name': test_name,
        'test_stage': test_stage,
        'model_name': model_name,
        'serial_number': serial_number,
        'status': status,
        'product': product,
        'start_date': start_date,
        'end_date': end_date,
        'tv_models': tv_models,
        'ac_models': ac_models,
        'phone_models': phone_models,
        'washing_machine_models': washing_machine_models,
    }
    return render(request, "dashboard_employee.html", context)

@login_required
def legal_dashboard(request):
    username = request.session['username']
    user = Employee.objects.get(username=username)
    if user.user_type != 'legal' and not user.is_superuser:
        return redirect('/access_denied/')
    # Get filter parameters from request
    test_name = request.GET.get('test_name', '')
    test_stage = request.GET.get('test_stage', '')
    product = request.GET.get('product', '')
    model_name = request.GET.get('model_name', '')
    serial_number = request.GET.get('serial_number', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    L_status = request.GET.get('L_status','')

    completed_tests = TestRecord.objects.exclude(L_status="Not Sent")
    if test_name:
        completed_tests = completed_tests.filter(TestName=test_name)
    if product:
        completed_tests = completed_tests.filter(ProductType=product)
    if test_stage:
        completed_tests = completed_tests.filter(TestStage=test_stage)
    if model_name:
        completed_tests = completed_tests.filter(ModelName=model_name)
    if serial_number:
        completed_tests = completed_tests.filter(SerailNo=serial_number)
    if L_status:
        completed_tests = completed_tests.filter(L_status= L_status)
    if start_date:
        completed_tests = completed_tests.filter(test_date__gte=start_date)
    if end_date:
        completed_tests = completed_tests.filter(test_date__lte=end_date)
    tests = completed_tests.values('ProductType', 'ModelName', 'TestStage').distinct()
    completed_tests = completed_tests.order_by('-test_date')

    tv_models = list(TV.objects.values_list('ModelName', flat=True))
    ac_models = list(AC.objects.values_list('ModelName', flat=True))
    phone_models = list(Phone.objects.values_list('ModelName', flat=True))
    washing_machine_models = list(WM_FATL.objects.values_list('ModelName', flat=True))
    test = json.dumps(list(TestRecord.objects.all().values()), cls=DjangoJSONEncoder)
    test = json.dumps(list(TestRecord.objects.all().values()), cls=DjangoJSONEncoder)
    context = {
        'test': test,
        'tests': tests,
        'all_tests': completed_tests,
        'test_name': test_name,
        'test_stage': test_stage,
        'model_name': model_name,
        'serial_number': serial_number,
        'L_status' : L_status,
        'product': product,
        'start_date': start_date,
        'end_date': end_date,
        'tv_models': tv_models,
        'ac_models': ac_models,
        'phone_models': phone_models,
        'washing_machine_models': washing_machine_models,
    }
    return render(request, "dashboard_legal.html", context)

@login_required
def brand_dashboard(request):
    username = request.session['username']
    user = Employee.objects.get(username=username)
    if user.user_type != 'brand' and not user.is_superuser:
        return redirect('/access_denied/')
    test_name = request.GET.get('test_name', '')
    test_stage = request.GET.get('test_stage', '')
    product = request.GET.get('product', '')
    model_name = request.GET.get('model_name', '')
    serial_number = request.GET.get('serial_number', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    B_status = request.GET.get('B_status','')
    completed_tests = TestRecord.objects.exclude(B_status="Not Sent")
    if test_name:
        completed_tests = completed_tests.filter(TestName=test_name)
    if product:
        completed_tests = completed_tests.filter(ProductType=product)
    if test_stage:
        completed_tests = completed_tests.filter(TestStage=test_stage)
    if model_name:
        completed_tests = completed_tests.filter(ModelName=model_name)
    if serial_number:
        completed_tests = completed_tests.filter(SerailNo=serial_number)
    if B_status:
        completed_tests = completed_tests.filter(B_status= B_status)
    if start_date:
        completed_tests = completed_tests.filter(test_date__gte=start_date)
    if end_date:
        completed_tests = completed_tests.filter(test_date__lte=end_date)

    tests = completed_tests.values('ProductType', 'ModelName', 'TestStage').distinct()
    completed_tests = completed_tests.order_by('-test_date')
    
    tv_models = list(TV.objects.values_list('ModelName', flat=True))
    ac_models = list(AC.objects.values_list('ModelName', flat=True))
    phone_models = list(Phone.objects.values_list('ModelName', flat=True))
    washing_machine_models = list(WM_FATL.objects.values_list('ModelName', flat=True))
    test = json.dumps(list(TestRecord.objects.all().values()), cls=DjangoJSONEncoder)
    context = {
        'test': test,
        'tests': tests,
        'all_tests': completed_tests,
        'test_name': test_name,
        'test_stage': test_stage,
        'model_name': model_name,
        'serial_number': serial_number,
        'B_status' : B_status,
        'product': product,
        'start_date': start_date,
        'end_date': end_date,
        'tv_models': tv_models,
        'ac_models': ac_models,
        'phone_models': phone_models,
        'washing_machine_models': washing_machine_models,
        'username': username
    }
    return render(request, "dashboard_brand.html", context)

@login_required
def legal_view(request, stage, product, test_name, model_name, serialno):
    user = Employee.objects.get(username=request.session['username'])
    if user.user_type != 'legal' and not user.is_superuser:
        return redirect('/access_denied/')
    Test_protocol = get_object_or_404(Test_core_detail, TestName=test_name, ProductType=product)
    # product = TestRecord.objects.get(ModelName=model_name, TestName=test_name, SerailNo=serialno, TestStage=stage).ProductType
    if product == 'AC':
        models = get_object_or_404(AC, ModelName=model_name)
    elif product == 'WM - FATL':
        models = get_object_or_404(WM_FATL, ModelName=model_name)
    test_record = get_object_or_404(TestRecord, ProductType=product, ModelName=model_name, SerailNo=serialno, TestStage=stage, TestName=test_name)
    page_break = '''<hr style="border-top: solid black; width: 100%;">'''
    soup = BeautifulSoup(test_record.additional_details, 'html.parser')
    paragraphs = soup.find_all('p')
    page_break_paragraphs = [p for p in paragraphs if p.text.strip().lower() == "pagebreak"]
    for p in page_break_paragraphs:
        p.string = ""
        p.append(BeautifulSoup(page_break, 'html.parser'))
    test_record.additional_details = str(soup)
    context = {
        'testdetail': test_record,
        'TestProtocol': Test_protocol,
        'model': models,
        'test': test_record,
        'test_name': test_name,
        'model_name': model_name,
        'serialno': serialno
    }
    return render(request, "legal_view.html", context)

@login_required
def brand_view(request, stage, product, test_name, model_name, serialno):
    user = Employee.objects.get(username=request.session['username'])
    if user.user_type != 'brand' and not user.is_superuser:
        return redirect('/access_denied/')
    Test_protocol = get_object_or_404(Test_core_detail, TestName=test_name, ProductType=product)
    # product = TestRecord.objects.get(ModelName=model_name, TestName=test_name, SerailNo=serialno, TestStage=stage).ProductType
    if product == 'AC':
        models = get_object_or_404(AC, ModelName=model_name)
    elif product == 'WM - FATL':
        models = get_object_or_404(WM_FATL, ModelName=model_name)
    test_record = get_object_or_404(TestRecord, ProductType=product, ModelName=model_name, SerailNo=serialno, TestStage=stage, TestName=test_name)
    page_break = '''<hr style="border-top: solid black; width: 100%;">'''
    soup = BeautifulSoup(test_record.additional_details, 'html.parser')
    paragraphs = soup.find_all('p')
    page_break_paragraphs = [p for p in paragraphs if p.text.strip().lower() == "pagebreak"]
    for p in page_break_paragraphs:
        p.string = ""
        p.append(BeautifulSoup(page_break, 'html.parser'))
    test_record.additional_details = str(soup)
    context = {
        'testdetail': test_record,
        'TestProtocol': Test_protocol,
        'model': models,
        'test': test_record,
        'test_name': test_name,
        'model_name': model_name,
        'serialno': serialno
    }
    return render(request, "brand_view.html", context)

@login_required
def MNF(request):
    user = Employee.objects.get(username=request.session['username'])
    if user.user_type != 'owner' and not user.is_superuser:
        return redirect('/access_denied/')
    if request.method == 'POST':
        customer = request.POST.get('Customer')
        manufacture = request.POST.get('Manufacture')
        location = request.POST.get('Location')
        brand = request.POST.get('Brand')
        Product = request.POST.get('Product')
        brand_model_no = request.POST.get('Brand_model_no')
        Indkal_model_no = request.POST.get('Indkal_model_no')
        ODM_model_no = request.POST.get('ODM_model_no')

        existing_mnf = Model_MNF_detail.objects.filter(Indkal_model_no=Indkal_model_no, Product=Product).first()
        if existing_mnf:
            messages.error(request, 'Model details already exist')
            return redirect('/dashboard/')

        new_mnf = Model_MNF_detail(
           Customer = customer,
           Manufacture = manufacture,
           Location = location,
           Brand = brand,
           Product = Product,
           Brand_model_no = brand_model_no,
           Indkal_model_no = Indkal_model_no,
           ODM_model_no = ODM_model_no
        )
        new_mnf.save()

        if Product == "AC":
            new_ac = AC.objects.create()
            new_ac.ModelName = Indkal_model_no
            new_ac.save()
        elif Product == "WM - FATL":
            new_wm = WM_FATL.objects.create()
            new_wm.ModelName = Indkal_model_no
            new_wm.save()
        else:
            return redirect('/access_denied/')

        if Product in Product_List.objects.values_list('Product', flat=True):
            return redirect(f'/prod/specs/{Indkal_model_no}/{Product}')
        else:
            return redirect('/access_denied/')
    
    products = Product_List.objects.values_list('Product', flat=True)
    context = {
        'products': list(products),
    }
    return render(request, 'productMNFdetail.html',context)

@login_required
def model_details_update(request):
    user = Employee.objects.get(username=request.session['username'])
    if user.user_type != 'owner' and not user.is_superuser:
        return redirect('/access_denied/')
    if request.method == 'POST':
        customer = request.POST.get('Customer')
        manufacture = request.POST.get('Manufacture')
        location = request.POST.get('Location')
        brand = request.POST.get('Brand')
        Product = request.POST.get('Product')
        brand_model_no = request.POST.get('Brand_model_no')
        Indkal_model_no = request.POST.get('Indkal_model_no')
        ODM_model_no = request.POST.get('ODM_model_no')

        existing_mnf = Model_MNF_detail.objects.get(Indkal_model_no=Indkal_model_no, Product=Product)
        if existing_mnf:
            existing_mnf.Customer = customer
            existing_mnf.Manufacture = manufacture
            existing_mnf.Location = location
            existing_mnf.Brand = brand
            existing_mnf.Product = Product
            existing_mnf.Brand_model_no = brand_model_no
            existing_mnf.Indkal_model_no = Indkal_model_no
            existing_mnf.ODM_model_no = ODM_model_no
            existing_mnf.save()
        else:
            messages.error(request, 'Model details do not exist')
            return redirect('/dashboard/')

        if Product in Product_List.objects.values_list('Product', flat=True):
            return redirect(f'/prod/specs/{Indkal_model_no}/{Product}')
        else:
            return redirect('/access_denied/')
    products = list(Product_List.objects.values_list('Product', flat=True))
    models = list(Model_MNF_detail.objects.values())
    context = {
        'products': products,
        'models': models,
    }
    return render(request, 'model_details_update.html',context)

@login_required
def model_details_view(request):
    user = Employee.objects.get(username=request.session['username'])
    if user.user_type != 'owner' and not user.is_superuser:
        return redirect('/access_denied/')
    if 'clear_filters' in request.GET:
        return redirect('model_details_view')
    product_filter = request.GET.get('product_filter', '')
    model_filter = request.GET.get('model_filter', '')
    products = Model_MNF_detail.objects.values_list('Product', flat=True).distinct()
    if product_filter:
        models = Model_MNF_detail.objects.filter(Product=product_filter).values_list('Indkal_model_no', flat=True).distinct()
    else:
        models = Model_MNF_detail.objects.values_list('Indkal_model_no', flat=True).distinct()
    filtered_models = Model_MNF_detail.objects.all()
    if product_filter:
        filtered_models = filtered_models.filter(Product=product_filter)
        if model_filter and not Model_MNF_detail.objects.filter(Product=product_filter, Indkal_model_no=model_filter).exists():
            model_filter = ''
            query_params = request.GET.copy()
            query_params['model_filter'] = ''
            return redirect(f"{request.path}?{query_params.urlencode()}")
    if model_filter:
        filtered_models = filtered_models.filter(Indkal_model_no=model_filter)
    context = {
        'modelnames': models,
        'products': products,
        'models': filtered_models,
        'product_filter': product_filter,
        'model_filter': model_filter,
    }
    return render(request, 'model_details_view.html', context)

@login_required
def to_dashboards(request):
    user = Employee.objects.get(username=request.session['username'])
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == "dashboard":
            if user.user_type=="owner":
                return redirect('/dashboard/')
            if user.user_type=="employee":
                return redirect('/employee_dashboard/')
            if user.user_type=="brand":
                return redirect('/brand_dashboard/')
            if user.user_type=="legal":
                return redirect('/legal_dashboard/')

@login_required
def Test_list_entry(request):
    user = Employee.objects.get(username=request.session['username'])
    if user.user_type != 'owner' and not user.is_superuser:
        return redirect('/access_denied/')
    if request.method == 'POST':
        testStages = request.POST.getlist('TestStage')
        product = request.POST.get('Product')
        testName = request.POST.get('TestName')

        s1 = ""
        if "DVT" in testStages:
            s1 += "1"
        else:
            s1 += "0"
        if "PP" in testStages:
            s1 += "1"
        else:
            s1 += "0"
        if "MP" in testStages:
            s1 += "1"
        else:
            s1 += "0"
        # existingProd = Product_List.objects.get(Product=product)
        # T = list(map(bool, [int(_) for _ in s1]))
        # S = ['DVT', 'PP', 'MP']
        # stages = [_ for i, _ in enumerate(S) if T[i]]
        # for s in stages:
        #     if testName not in existingProd.Test_Names[s]:
        #         existingProd.Test_Names[s].append(testName)
        # existingProd.save()
        new_test = Test_core_detail(
            TestStage=s1,
            ProductType=product,
            TestName=testName,
        )
        new_test.save()
        return redirect(reverse('test_protocol_entry', args=[testName, product]))

    products = list(Product_List.objects.values_list('Product', flat=True))
    context = {
        'products': products,
    }
    return render(request, 'Test_list_entry.html',context)

@login_required
def test_protocol_entry(request, test_name, product):
    user = Employee.objects.get(username=request.session['username'])
    if user.user_type != 'owner' and not user.is_superuser:
        return redirect('/access_denied/')
    if request.method == 'POST':
        testobjective = request.POST.get('Testobjective')
        teststandard = request.POST.get('Teststandard')
        testcondition = request.POST.get('Testcondition')
        testprocedure = request.POST.get('Testprocedure')
        judgement = request.POST.get('judgement')
        instrument = request.POST.get('instrument')

        existing_test = Test_core_detail.objects.filter(TestName=test_name, ProductType=product).first()
        existing_test.Test_Objective=testobjective
        existing_test.Test_Standard=teststandard
        existing_test.Test_Condition=testcondition
        existing_test.Test_Procedure=testprocedure
        existing_test.Judgement=judgement
        existing_test.Instrument=instrument
        existing_test.save()
        messages.success(request, 'Test protocols added.')
        return redirect('/dashboard/')  
    test_detail = Test_core_detail.objects.get(TestName=test_name, ProductType=product)
    context = {
    'test_name': test_name,
    'product': product,
    'test_detail': test_detail,
    }
    return render(request, 'test_protocol_entry.html', context)

@login_required
def update_test_list_entry(request):
    user = Employee.objects.get(username=request.session['username'])
    if user.user_type != 'owner' and not user.is_superuser:
        return redirect('/access_denied/')
    if request.method == 'POST':
        testStages = request.POST.getlist('TestStage')
        product = request.POST.get('Product')
        testName = request.POST.get('TestName')
        # Check if a test with the same name already exists
        existing_test = Test_core_detail.objects.filter(TestName=testName, ProductType=product).first()
        s1 = ""
        if "DVT" in testStages:
            s1 += "1"
        else:
            s1 += "0"
        if "PP" in testStages:
            s1 += "1"
        else:
            s1 += "0"
        if "MP" in testStages:
            s1 += "1"
        else:
            s1 += "0"

        if existing_test:
            existing_test.TestStage = s1
            existing_test.save()
        return redirect(reverse('test_protocol_entry', args=[testName, product]))

    test_names = Test_core_detail.objects.values_list('TestName', flat=True).distinct()
    products = list(Product_List.objects.values_list('Product', flat=True))
    test = list(Test_core_detail.objects.all().values())
    context = {
        'test': test,
        'test_names': test_names,
        'products': products,
    }
    return render(request, 'Update_Test_list_entry.html', context)

@login_required
def test_details_view(request):
    user = Employee.objects.get(username=request.session['username'])
    if user.user_type != 'owner' and not user.is_superuser:
        return redirect('/access_denied/')
    if 'clear_filters' in request.GET:
        return redirect('test_details_view')
    product_filter = request.GET.get('product_filter', '')
    model_filter = request.GET.get('model_filter', '')
    products = Test_core_detail.objects.values_list('ProductType', flat=True).distinct()
    if product_filter:
        testnames = Test_core_detail.objects.filter(ProductType=product_filter).values_list('TestName', flat=True).distinct()
    else:
        testnames = Test_core_detail.objects.values_list('TestName', flat=True).distinct()
    filtered_tests = Test_core_detail.objects.all()
    if product_filter:
        filtered_tests = filtered_tests.filter(ProductType=product_filter)
        if model_filter and not Test_core_detail.objects.filter(ProductType=product_filter, TestName=model_filter).exists():
            model_filter = ''
            query_params = request.GET.copy()
            query_params['model_filter'] = ''
            return redirect(f"{request.path}?{query_params.urlencode()}")
    if model_filter:
        filtered_tests = filtered_tests.filter(TestName=model_filter)
    context = {
        'tests': filtered_tests,
        'products': products,
        'testnames': testnames,
        'product_filter': product_filter,
        'model_filter': model_filter,
    }
    return render(request, 'test_details_view.html', context)

def ckeditor_image_upload(request):
    user = request.session['username']
    if request.method == 'POST' and request.FILES:
        if request.FILES['ckeditor_image_upload'].content_type.startswith('image/'):
            file = request.FILES['ckeditor_image_upload']
            today = dt.now()
            upload_dir = os.path.join('ckeditor', user, str(today.year), str(today.month), str(today.day))
            os.makedirs(upload_dir, exist_ok=True)
            file_name = default_storage.save(os.path.join(upload_dir, file.name), ContentFile(file.read()))
            file_url = default_storage.url(file_name)
            response = {
                'uploaded': True,
                'url': file_url
            }
            return JsonResponse(response)
        print("didn't run upload request")
        return JsonResponse({'error': 'Invalid file type. Only images are allowed.'}, status=422)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def server_media_browse(request):
    username = request.session['username']
    user_dir = os.path.join(settings.MEDIA_ROOT, 'ckeditor', username)

    # Filtering files by date (if date filter is applied)
    filter_date = request.GET.get('date')
    files = []
    
    for root, dirs, filenames in os.walk(user_dir):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            file_url = os.path.relpath(file_path, settings.MEDIA_ROOT)
            file_stat = os.stat(file_path)
            file_date = dt.fromtimestamp(file_stat.st_mtime)
            
            if filter_date and file_date.strftime('%Y-%m-%d') != filter_date:
                continue

            files.append({
                'name': filename,
                'url': file_url.replace('\\', '/'),
                'date': file_date,
                'size': file_stat.st_size / 1024,
            })
    
    # Sorting files by date or name
    sort_by = 'date'  # Only sorting by date as per requirement
    reverse = request.GET.get('order', 'desc') == 'desc'
    files.sort(key=lambda x: x[sort_by], reverse=reverse)

    context = {
        'MEDIA_URL': settings.MEDIA_URL,
        'files': files,
        'filter_date': filter_date,
        'order': 'asc' if not reverse else 'desc',
    }
    
    return render(request, 'media_browse.html', context)

@login_required
def handle_notification(request):
    if request.method == 'POST':
        inc_notif = json.loads(request.body)
        user = Employee.objects.get(username=request.session['username'])
        notification = Notification.objects.get(employee=user.username)
        for i in range(len(notification.notification)):
            notify = json.loads(notification.notification[i])
            if notify["metadata"] == inc_notif["metadata"] and notify['action'] == inc_notif['action'] and not notify['is_read'] and notify["created_at"] == inc_notif["created_at"]:
                notification.unread_count -= 1
                notify['is_read'] = True
                notification.notification[i] = json.dumps(notify)
                break
        notification.save()
        if user.user_type == 'owner':
            if inc_notif['action'] == 'sent-1':
                redirect_url = f'/owner_view/{inc_notif["metadata"]["test"]}/{inc_notif["metadata"]["model"]}/{inc_notif["metadata"]["serialno"]}'
            elif inc_notif['action'] in ['approved', 'rejected']:
                redirect_url = f'/owner_view/{inc_notif["metadata"]["test"]}/{inc_notif["metadata"]["model"]}/{inc_notif["metadata"]["serialno"]}'
        elif user.user_type == 'employee':
            if inc_notif['action'] in ['approved', 'rejected']:
                redirect_url = f'/view/{inc_notif["metadata"]["test"]}/{inc_notif["metadata"]["model"]}/{inc_notif["metadata"]["serialno"]}'
        elif user.user_type == 'brand':
            if inc_notif['action'] == 'sent':
                redirect_url = f'/brand_dashboard/?product={inc_notif["metadata"]["product"]}&test_stage={inc_notif["metadata"]["stage"]}&model_name={inc_notif["metadata"]["model"]}'
            elif inc_notif['action'] == 'sent-1':
                redirect_url = f'/brand_view/{inc_notif["metadata"]["test"]}/{inc_notif["metadata"]["model"]}/{inc_notif["metadata"]["serialno"]}'
        elif user.user_type == 'legal':
            if inc_notif['action'] == 'sent':
                redirect_url = f'/legal_dashboard/?product={inc_notif["metadata"]["product"]}&test_stage={inc_notif["metadata"]["stage"]}&model_name={inc_notif["metadata"]["model"]}'
            elif inc_notif['action'] == 'sent-1':
                redirect_url = f'/legal_view/{inc_notif["metadata"]["test"]}/{inc_notif["metadata"]["model"]}/{inc_notif["metadata"]["serialno"]}'
        return JsonResponse({'redirect_url': redirect_url})
    return HttpResponse('Invalid request method')

def clear_notification(request):
    if request.method == 'POST':
        inc_notif = json.loads(request.body)["notification"]
        user = Employee.objects.get(username=request.session['username'])
        notification = Notification.objects.get(employee=user.username)
        for i in range(len(notification.notification)):
            notify = json.loads(notification.notification[i])
            if inc_notif == 'all' or (notify["metadata"] == inc_notif["metadata"] and notify['action'] == inc_notif['action']):
                notify['is_cleared'] = True
            notification.notification[i] = json.dumps(notify)
        notification.save()
        return HttpResponse('Notification cleared successfully')
    return HttpResponse('Invalid request method')

@login_required
def notifications(request):
    notification = Notification.objects.get(employee=request.session['username'])
    latest_notifications = notification.notification[::-1]
    notif_list = []
    for notif in latest_notifications:
        notify = json.loads(notif)
        created_at = dt.strptime(notify['created_at'], "%Y-%m-%d %H:%M:%S")
        time_diff = dt.now() - created_at
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
    context = {
        'notifications': notif_list,
    }
    return render(request, 'notifications.html', context=context)