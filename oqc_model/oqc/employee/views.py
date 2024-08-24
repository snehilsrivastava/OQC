from datetime import date
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.http import Http404, QueryDict
from .forms import *
from .models import *
from .renderers import *
from product.views import *
from authapp.models import Employee
from authapp.views import login_page
import PyPDF2
from io import BytesIO
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Min, Max, Case, When, DateField

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        next_page = request.original_path
        if 'username' in request.session:
            return view_func(request, *args, **kwargs)
        login_url = '/au/login'
        return redirect(f"{login_url}?next={next_page}" if next_page else login_url)
    return wrapper

@login_required
def access_denied(request):
    user = request.session['username']
    employee = Employee.objects.get(username=user)
    icon = employee.first_name[0] + employee.last_name[0]
    context = {
        'user': employee,
        'first_name': employee.first_name,
        'last_name': employee.last_name,
        'icon': icon,
    }
    return render(request, "access_denied.html", context=context)

@login_required
def custom_404(request, exception):
    user = request.session['username']
    employee = Employee.objects.get(username=user)
    icon = employee.first_name[0] + employee.last_name[0]
    context = {
        'user': employee,
        'first_name': employee.first_name,
        'last_name': employee.last_name,
        'icon': icon,
    }
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
    if test_record.employee != user.username and not user.is_superuser:
        return redirect('/access_denied/')
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
    username = request.session['username']
    employee = Employee.objects.get(username=username)
    icon = employee.first_name[0] + employee.last_name[0]

    context = {
        'first_name': employee.first_name,
        'last_name': employee.last_name,
        'icon': icon,
        'username': username,
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
    username = request.session['username']
    employee = Employee.objects.get(username=username)
    icon = employee.first_name[0] + employee.last_name[0]

    context = {
        'first_name': employee.first_name,
        'last_name': employee.last_name,
        'icon': icon,
        'username': username,
        'TestObjectRemark': TestObject,
    }
    return render(request, "owner_remark.html", context)

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
    
    completed_tests = TestRecord.objects.filter(employee=username)

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
    employee = Employee.objects.get(username=username)
    icon = employee.first_name[0] + employee.last_name[0]
    context = {
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
        'first_name': employee.first_name,
        'last_name': employee.last_name,
        'icon': icon,
        'username': username
    }
    return render(request, "dashboard_employee.html", context)

@login_required
def report(request, test_name, model_name, serialno):
    user = Employee.objects.get(username=request.session['username'])
    if (user.user_type != 'employee' and user.user_type != 'owner') and not user.is_superuser:
        return redirect('/access_denied/')
    Test_protocol = get_object_or_404(Test_core_detail, TestName=test_name)
    product = TestRecord.objects.get(ModelName=model_name, TestName=test_name, SerailNo=serialno).ProductType
    if product == 'AC':
        models = get_object_or_404(AC, ModelName=model_name)
    elif product == 'WM - FATL':
        models = get_object_or_404(WM_FATL, ModelName=model_name)
    test_record = get_object_or_404(TestRecord, SerailNo=serialno, TestName=test_name, ModelName=model_name)
    if test_record.employee != user.username and not user.is_superuser:
        return redirect('/access_denied/')
    if request.method == 'POST':
        form = TestRecordForm(request.POST, instance=test_record)  
        if form.is_valid():
            form.save()
            messages.success(request, 'Test record saved successfully.')
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
    if test_record.employee != user.username and not user.is_superuser:
        return redirect('/access_denied/')
    test_record.status = "Waiting"
    test_record.test_end_date = date.today()
    test_record.test_date = date.today()
    test_record.save()
    messages.success(request, 'Record sent to PO for approval.')
    return redirect('/employee_dashboard/')

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
    status_color = {"Not Sent": "#838383", "Waiting": "Yellow", "Approved": "#5AA33F", "Rejected": "Red"}
    role_letter = {"T": "Test Inspector", "L": "Legal Team", "B": "Brand Team"}

    completed_tests = TestRecord.objects.exclude(status="Not Sent")
    if test_name:
        completed_tests = completed_tests.filter(TestName__icontains=test_name)
    if product:
        completed_tests = completed_tests.filter(ProductType__icontains=product)
    if test_stage:
        completed_tests = completed_tests.filter(TestStage__icontains=test_stage)
    if model_name:
        completed_tests = completed_tests.filter(ModelName__icontains=model_name)
    if serial_number:
        completed_tests = completed_tests.filter(SerailNo__icontains=serial_number)
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
    tests = completed_tests.values('ProductType', 'ModelName', 'TestStage').distinct()
    completed_tests = completed_tests.order_by('-test_end_date')
    tv_models = list(TV.objects.values_list('ModelName', flat=True))
    ac_models = list(AC.objects.values_list('ModelName', flat=True))
    phone_models = list(Phone.objects.values_list('ModelName', flat=True))
    washing_machine_models = list(WM_FATL.objects.values_list('ModelName', flat=True))
    employee = user
    icon = employee.first_name[0] + employee.last_name[0]
    context = {
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
        'tv_models': tv_models,
        'ac_models': ac_models,
        'phone_models': phone_models,
        'washing_machine_models': washing_machine_models,
        'first_name': employee.first_name,
        'last_name': employee.last_name,
        'icon': icon,
        'username': username,
        'status_color' : status_color,
        'role_letter': role_letter
    }
    return render(request, 'dashboard_PO.html', context)

from django.contrib.auth import logout as auth_logout

@login_required
def logout(request):
    if request.method == "POST":
        auth_logout(request)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@login_required
def edit(request, test_name, model_name, serialno):
    user = Employee.objects.get(username=request.session['username'])
    if user.user_type != 'employee' and not user.is_superuser:
        return redirect('/access_denied/')
    Test_protocol = get_object_or_404(Test_core_detail, TestName=test_name)
    product = TestRecord.objects.get(ModelName=model_name, TestName=test_name, SerailNo=serialno).ProductType
    if product == 'AC':
        models = get_object_or_404(AC, ModelName=model_name)
    elif product == 'WM - FATL':
        models = get_object_or_404(WM_FATL, ModelName=model_name)
    test_record = get_object_or_404(TestRecord, SerailNo=serialno, TestName=test_name, ModelName=model_name)
    if test_record.employee != user.username and not user.is_superuser:
        return redirect('/access_denied/')
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
        'serialno': serialno
    }
    return render(request, "report.html", context)

@login_required
def view_pdf(request, test_name, model_name, serialno):
    Test_protocol = get_object_or_404(Test_core_detail, TestName=test_name)
    product = TestRecord.objects.get(ModelName=model_name, TestName=test_name, SerailNo=serialno).ProductType
    if product == 'AC':
        models = get_object_or_404(AC, ModelName=model_name)
    elif product == 'WM - FATL':
        models = get_object_or_404(WM_FATL, ModelName=model_name)
    test_record = get_object_or_404(TestRecord, SerailNo=serialno)
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

        elif action == 'send_brand':
            if not selected_test_records.exists():
                messages.error(request, 'No test records selected')
                return redirect('/dashboard/')   
            for test_record in selected_test_records:
                if test_record.B_status != "Approved":
                    test_record.B_status = "Waiting"
                test_record.owner_name = user.first_name + " " + user.last_name
                test_record.save()
            messages.success(request, 'Sent to Bran d Team for approval.')

        elif action == 'send_legal':
            if not selected_test_records.exists():
                messages.error(request, 'No test records selected')
                return redirect('/dashboard/')   
            for test_record in selected_test_records:
                if test_record.L_status != "Approved":
                    test_record.L_status = "Waiting"
                test_record.owner_name = user.first_name + " " + user.last_name
                test_record.save()
            messages.success(request, 'Sent to Legal Team for approval.')

    if user.user_type=='owner':      
        return redirect('/dashboard/')
    elif user.user_type=='legal':      
        return redirect('/legal_dashboard/')
    elif user.user_type=='brand':      
        return redirect('/brand_dashboard/')

@login_required
def view(request, test_name, model_name, serialno):
    user = Employee.objects.get(username=request.session['username'])
    if user.user_type != 'employee' and not user.is_superuser:
        return redirect('/access_denied/')
    Test_protocol = get_object_or_404(Test_core_detail, TestName=test_name)
    product = TestRecord.objects.get(ModelName=model_name, TestName=test_name, SerailNo=serialno).ProductType
    if product == 'AC':
        models = get_object_or_404(AC, ModelName=model_name)
    elif product == 'WM - FATL':
        models = get_object_or_404(WM_FATL, ModelName=model_name)
    test_record = get_object_or_404(TestRecord, SerailNo=serialno , TestName =test_name)
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
def owner_view(request, test_name, model_name, serialno):
    user = Employee.objects.get(username=request.session['username'])
    if user.user_type != 'owner' and not user.is_superuser:
        return redirect('/access_denied/')
    Test_protocol = get_object_or_404(Test_core_detail, TestName=test_name)
    product = TestRecord.objects.get(ModelName=model_name, TestName=test_name, SerailNo=serialno).ProductType
    if product == 'AC':
        models = get_object_or_404(AC, ModelName=model_name)
    elif product == 'WM - FATL':
        models = get_object_or_404(WM_FATL, ModelName=model_name)
    test_record = get_object_or_404(TestRecord, SerailNo=serialno, ModelName=model_name, TestName=test_name)
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
    if status == 1:
        test.status = 'Waiting'
    elif status == 2:
        test.status = 'Approved'
    else:
        test.status = 'Rejected'
    test.save()
    test_name = test.TestName
    model_name = test.ModelName
    serialno = test.SerailNo
    return redirect('owner_view', test_name=test_name, model_name=model_name, serialno=serialno)

@login_required
def change_status_legal(request, test_id, status):
    user = Employee.objects.get(username=request.session['username'])
    if user.user_type != 'legal' and not user.is_superuser:
        return redirect('/access_denied/')
    test = get_object_or_404(TestRecord, id=test_id)
    if status == 1:
        test.L_status = "Waiting"
    elif status == 2:
        test.L_status = "Approved"
    else:
        test.L_status = "Rejected"
    test.save()
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
    if status == 1:
        test.B_status = "Waiting"
    elif status == 2:
        test.B_status = "Approved"
    else:
        test.B_status = "Rejected"
    test.save()
    test_name = test.TestName
    model_name = test.ModelName
    serialno = test.SerailNo
    return redirect('brand_view', test_name=test_name, model_name=model_name, serialno=serialno)

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
        completed_tests = completed_tests.filter(TestName__icontains=test_name)
    if product:
        completed_tests = completed_tests.filter(ProductType__icontains=product)
    if test_stage:
        completed_tests = completed_tests.filter(TestStage__icontains=test_stage)
    if model_name:
        completed_tests = completed_tests.filter(ModelName__icontains=model_name)
    if serial_number:
        completed_tests = completed_tests.filter(SerailNo__icontains=serial_number)
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
    employee = Employee.objects.get(username=username)
    icon = employee.first_name[0] + employee.last_name[0]
    context = {
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
        'first_name': employee.first_name,
        'last_name': employee.last_name,
        'icon': icon,
        'username': username
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
        completed_tests = completed_tests.filter(TestName__icontains=test_name)
    if product:
        completed_tests = completed_tests.filter(ProductType__icontains=product)
    if test_stage:
        completed_tests = completed_tests.filter(TestStage__icontains=test_stage)
    if model_name:
        completed_tests = completed_tests.filter(ModelName__icontains=model_name)
    if serial_number:
        completed_tests = completed_tests.filter(SerailNo__icontains=serial_number)
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
    employee = Employee.objects.get(username=username)
    icon = employee.first_name[0] + employee.last_name[0]
    context = {
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
        'first_name': employee.first_name,
        'last_name': employee.last_name,
        'icon': icon,
        'username': username
    }
    return render(request, "dashboard_brand.html", context)

@login_required
def legal_view(request, test_name, model_name, serialno):
    user = Employee.objects.get(username=request.session['username'])
    if user.user_type != 'legal' and not user.is_superuser:
        return redirect('/access_denied/')
    Test_protocol = get_object_or_404(Test_core_detail, TestName=test_name)
    product = TestRecord.objects.get(ModelName=model_name, TestName=test_name, SerailNo=serialno).ProductType
    if product == 'AC':
        models = get_object_or_404(AC, ModelName=model_name)
    elif product == 'WM - FATL':
        models = get_object_or_404(WM_FATL, ModelName=model_name)
    test_record = get_object_or_404(TestRecord, SerailNo=serialno)
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
def brand_view(request, test_name, model_name, serialno):
    user = Employee.objects.get(username=request.session['username'])
    if user.user_type != 'brand' and not user.is_superuser:
        return redirect('/access_denied/')
    Test_protocol = get_object_or_404(Test_core_detail, TestName=test_name)
    product = TestRecord.objects.get(ModelName=model_name, TestName=test_name, SerailNo=serialno).ProductType
    if product == 'AC':
        models = get_object_or_404(AC, ModelName=model_name)
    elif product == 'WM - FATL':
        models = get_object_or_404(WM_FATL, ModelName=model_name)
    test_record = get_object_or_404(TestRecord, SerailNo=serialno)
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
        Product= request.POST.get('Product')
        brand_model_no = request.POST.get('Brand_model_no')
        Indkal_model_no = request.POST.get('Indkal_model_no')
        ODM_model_no = request.POST.get('ODM_model_no')
     
        new_mnf = Model_MNF_detail(
           Customer = customer,
           Manufacture = manufacture,
           Location = location,
           Brand = brand,
           Product= Product,
           Brand_model_no = brand_model_no,
           Indkal_model_no = Indkal_model_no,
           ODM_model_no = ODM_model_no

        )
        new_mnf.save()
        if Product == 'AC':
            username = request.session['username']
            employee = Employee.objects.get(username=username)
            icon = employee.first_name[0] + employee.last_name[0]
            context = {
            'first_name': employee.first_name,
            'last_name': employee.last_name,
            'icon': icon,
            'username': username,
            'Indkal_model_no': Indkal_model_no,
            }
            return render(request, 'AC.html', context)
        else:
            return redirect('/access_denied/')
    
    username = request.session['username']
    employee = Employee.objects.get(username=username)
    icon = employee.first_name[0] + employee.last_name[0]
    products = Test_core_detail.objects.values_list('ProductType', flat=True).distinct()
    context = {
        'first_name': employee.first_name,
        'last_name': employee.last_name,
        'icon': icon,
        'username': username,
        'products': products,
    }
    return render(request, 'productMNFdetail.html',context)

@login_required
def model_details_view(request):
    username = request.session['username']
    user = Employee.objects.get(username=username)
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

    icon = user.first_name[0] + user.last_name[0]
    context = {
        'modelnames': models,
        'products': products,
        'models': filtered_models,
        'product_filter': product_filter,
        'model_filter': model_filter,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'icon': icon,
        'username': username,
    }
    return render(request, 'model_details_view.html', context)

@login_required
def Test_list_entry(request):
    user = Employee.objects.get(username=request.session['username'])
    if user.user_type != 'owner' and not user.is_superuser:
        return redirect('/access_denied/')
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
        if "PDI" in testStages:
            s1 += "1"
        else:
            s1 += "0"
        existing_test = Test_core_detail.objects.filter(TestName=testName, ProductType=product).first()
        if existing_test:
            existing_test.TestStage = s1
            existing_test.save()
        else:
            new_test = Test_core_detail(
                TestStage=s1,
                ProductType=product,
                TestName=testName,
            )
            new_test.save()

        return redirect(reverse('test_protocol_entry', args=[testName, product]))
    
    username = request.session['username']
    employee = user
    icon = employee.first_name[0] + employee.last_name[0]
    products = list(Test_core_detail.objects.values_list('ProductType', flat=True).distinct())
    context = {
        'first_name': employee.first_name,
        'last_name': employee.last_name,
        'icon': icon,
        'username': username,
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

        # Check if the test detail info already exists
        if Test_core_detail.objects.filter(TestName=test_name, ProductType=product).exists():
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

        # never going to be executed ?
        test_detail = Test_core_detail(
            ProductType=product,
            TestName=test_name,
            Test_Objective=testobjective,
            Test_Standard=teststandard,
            Test_Condition=testcondition,
            Test_Procedure=testprocedure,
            Judgement=judgement,
            Instrument=instrument,
            TestStage="1111",
        )
        test_detail.save()
        messages.success(request, 'Test protocols added!')
        return redirect('/dashboard/')

    username = request.session['username']
    employee = user
    icon = employee.first_name[0] + employee.last_name[0]
    try:
        test_detail = Test_core_detail.objects.get(TestName=test_name, ProductType=product)
    except Test_core_detail.DoesNotExist:
        test_detail = None
    context = {
    'first_name': employee.first_name,
    'last_name': employee.last_name,
    'icon': icon,
    'username': username,
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
        if "PDI" in testStages:
            s1 += "1"
        else:
            s1 += "0"

        if existing_test:
            existing_test.TestStage = s1
            existing_test.save()
        return redirect(reverse('test_protocol_entry', args=[testName, product]))

    test_names = Test_core_detail.objects.values_list('TestName', flat=True).distinct()
    products = list(Test_core_detail.objects.values_list('ProductType', flat=True).distinct())
    username = request.session['username']
    employee = user
    icon = employee.first_name[0] + employee.last_name[0]
    context = {
        'test_names': test_names,
        'products': products,
        'first_name': employee.first_name,
        'last_name': employee.last_name,
        'icon': icon,
        'username': username,
    }
    return render(request, 'Update_Test_list_entry.html', context)

@login_required
def test_details_view(request):
    username = request.session['username']
    user = Employee.objects.get(username=username)
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

    icon = user.first_name[0] + user.last_name[0]
    context = {
        'tests': filtered_tests,
        'products': products,
        'testnames': testnames,
        'product_filter': product_filter,
        'model_filter': model_filter,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'icon': icon,
        'username': username,
    }
    return render(request, 'test_details_view.html', context)