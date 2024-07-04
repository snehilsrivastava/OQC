from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.http import Http404
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

def main_page(request):
    return redirect(login_page)

def send_report(request, report_id):
    if request.method == 'GET':
        report = get_object_or_404(TestRecord, pk=report_id)
        # Update the report status to indicate it has been sent
        report.status = 'Sent to Owner'
        report.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def delete_test_record(request, record_id):
    try:
        # Get the TestRecord instance
        test_record = get_object_or_404(TestRecord, pk=record_id)
        
        # Perform deletion
        test_record.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
def remark(request, id):
    TestObjectRemark = get_object_or_404(TestRecord, pk=id)
    if request.method == 'POST':
       
        if 'employee-remark' in request.POST:
            TestObjectRemark.employee_remark = request.POST.get('employee-remark')
        TestObjectRemark.save()
        return redirect('/check/')  # Adjust this to your actual view name

    context = {
        'TestObjectRemark': TestObjectRemark,
    }
    return render(request, "remark.html", context)

def owner_remark(request, id):
    TestObjectRemark = get_object_or_404(TestRecord, pk=id)
    if request.method == 'POST':
       
        if 'product-owner-remark' in request.POST:
            TestObjectRemark.owner_remark = request.POST.get('product-owner-remark')
        TestObjectRemark.save()
        return redirect('/dashboard/')  # Adjust this to your actual view name

    context = {
        'TestObjectRemark': TestObjectRemark,
    }
    return render(request, "owner_remark.html", context)

def check(request):
    username = request.session['username']
    print(username)
    # Get filter parameters from request
    test_name = request.GET.get('test_name', '')
    test_stage = request.GET.get('test_stage', '')
    product = request.GET.get('product','')
    model_name = request.GET.get('model_name', '')
    serial_number = request.GET.get('serial_number', '')
    status = request.GET.get('status', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    
    # Filter the TestRecord queryset based on the parameters
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
    completed_tests = completed_tests.order_by('-test_date')
    tv_models = list(TV.objects.values_list('ModelName', flat=True))
    ac_models = list(AC.objects.values_list('ModelName', flat=True))
    phone_models = list(Phone.objects.values_list('ModelName', flat=True))
    washing_machine_models = list(Washing_Machine.objects.values_list('ModelName', flat=True))
    test = list(TestList.objects.all().values())
    employee = Employee.objects.get(username=username)
    icon = employee.first_name[0] + employee.last_name[0]
    context = {
        'completed_tests': completed_tests,
        'test_name': test_name,
        'test_stage': test_stage,
        'model_name': model_name,
        'serial_number': serial_number,
        'status': status,
        'product':product,
        'start_date': start_date,
        'end_date': end_date,
        'tv_models': tv_models,
        'ac_models': ac_models,
        'phone_models': phone_models,
        'washing_machine_models': washing_machine_models,
        'test' : test,
        'first_name' : employee.first_name,
        'last_name' : employee.last_name,
        'icon' : icon,
        'username' :username
    }

    return render(request, "test_report.html", context)

def cooling(request, test_name, model_name, serialno):
    # Fetch the specific Test_core_detail object related to the cooling test
    Test_protocol = get_object_or_404(Test_core_detail, TestName=test_name)
    models = get_object_or_404(AC, ModelName=model_name)
    test_record = get_object_or_404(TestRecord, SerailNo=serialno, TestName=test_name, ModelName=model_name)

    if request.method == 'POST':
        form = TestRecordForm(request.POST, instance=test_record)  
        if form.is_valid():
            # print("random")
            form.save()
        else:
            print(form.errors)
       
        return redirect('/check/')  # Redirect to a success page or another view
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
    return render(request, "cooling_test.html", context)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def toggle_status(request, id):
    if request.method == 'POST':
        try:
            test_record = TestRecord.objects.get(id=id)
            # Cycle through the statuses or implement your own logic
            new_status = ((test_record.status) % 3)+1
            test_record.status = new_status
            test_record.save()
            return JsonResponse({'success': True, 'new_status': new_status})
        except TestRecord.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Test record not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def set_status(request, id):
    if request.method == 'POST':
        try:
            test_record = TestRecord.objects.get(id=id)
            # Cycle through the statuses or implement your own logic
            new_status = 1
            test_record.status = new_status
            test_record.save()
            return JsonResponse({'success': True, 'new_status': new_status})
        except TestRecord.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Test record not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def view_test_report(request,pk):
    record = get_object_or_404(TestRecord, pk =pk)
    images = record.images.all()  # Fetch all images related to this record
    return render(request, 'view_record.html', {'record': record, 'images': images})

def dashboard(request):

    username = request.session['username']

    # Get filter parameters from request
    test_name = request.GET.get('test_name', '')
    test_stage = request.GET.get('test_stage', '')
    product = request.GET.get('product','')
    model_name = request.GET.get('model_name', '')
    serial_number = request.GET.get('serial_number', '')
    status = request.GET.get('status', '')
    L_status = request.GET.get('L_status', '')
    B_status = request.GET.get('B_status', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    status_color = {"Not Sent": "#b331a4", "Waiting for Approval": "Yellow", "Approved": "#5AA33F", "Rejected": "Red"}
    role_letter = {"L": "Legal Team", "B": "Brand Team", "O": "Product Owner"}

    # Filter the TestRecord queryset based on the parameters
    completed_tests = TestRecord.objects.filter()

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
        completed_tests = completed_tests.filter(status=(status.lower() == 'complete'))
    if start_date:
        completed_tests = completed_tests.filter(test_date__gte=start_date)
    if end_date:
        completed_tests = completed_tests.filter(test_date__lte=end_date)
    completed_tests = completed_tests.order_by('-test_date')
    tv_models = list(TV.objects.values_list('ModelName', flat=True))
    ac_models = list(AC.objects.values_list('ModelName', flat=True))
    phone_models = list(Phone.objects.values_list('ModelName', flat=True))
    washing_machine_models = list(Washing_Machine.objects.values_list('ModelName', flat=True))

    context = {
        'completed_tests': completed_tests,
        'test_name': test_name,
        'test_stage': test_stage,
        'model_name': model_name,
        'serial_number': serial_number,
        'status': status,
        'L_status': L_status,
        'B_status': B_status,
        'product':product,
        'start_date': start_date,
        'end_date': end_date,
        'tv_models': tv_models,
        'ac_models': ac_models,
        'phone_models': phone_models,
        'washing_machine_models': washing_machine_models,
        'status_color' : status_color,
        'role_letter': role_letter
    }

    return render(request, 'PO_dashboard.html', context)

from django.http import JsonResponse
from django.contrib.auth import logout as auth_logout

def logout(request):
    if request.method == "POST":
        auth_logout(request)  # Use the correct logout method from django.contrib.auth
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


def submit_product_details_view(request):
    return HttpResponse("Thank you for submitting product details")

def edit(request, test_name, model_name, serialno):
    # Fetch the specific Test_core_detail object related to the cooling test
    Test_protocol = get_object_or_404(Test_core_detail, TestName=test_name)
    models = get_object_or_404(AC, ModelName=model_name)
    # multiple test records might have same serial no.
    test_record = get_object_or_404(TestRecord, SerailNo=serialno, TestName=test_name, ModelName=model_name)

    if request.method == 'POST':
        form = TestRecordForm(request.POST, instance=test_record)  
        if form.is_valid():
            # print("random")
            form.save()
        else:
            print(form.errors)

        messages.success(request, 'Test record updated.')
        return redirect('/check/')  # Redirect to a success page or another view
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
    return render(request, "cooling_test.html", context)

def view_pdf(request, test_name, model_name, serialno):
    # Fetch the specific Test_core_detail object related to the cooling test
    Test_protocol = get_object_or_404(Test_core_detail, TestName=test_name)
    models = get_object_or_404(AC, ModelName=model_name)
    test_record = get_object_or_404(TestRecord, SerailNo=serialno)
    context = {
        'TestProtocol': Test_protocol,
        'model': models,
        'test': test_record,
    }
    return render(request, "view_pdf.html", context)


def merge_pdfs(pdf_list):
    merger = PyPDF2.PdfMerger()
    for pdf in pdf_list:
        pdf.seek(0)
        merger.append(pdf)

    merged_pdf_io = BytesIO()
    merger.write(merged_pdf_io)
    merged_pdf_io.seek(0)
    return merged_pdf_io

def generate_pdf(request):
    if request.method == 'POST':
        selected_test_ids = request.POST.getlist('selected_tests')
        # Retrieve the selected test records from the database
        selected_test_records = TestRecord.objects.filter(pk__in=selected_test_ids)
        if not selected_test_records.exists():
            raise Http404("No test records found")
        pdf_list = []
        cumul_page_count, cumul_page_count_list = 3, []
        test_name_list = []
        for i, test_record in enumerate(selected_test_records, start=1):
            model_name = test_record.ModelName
            test_name = test_record.TestName
            Test_protocol = get_object_or_404(Test_core_detail, TestName=test_name)
            models = get_object_or_404(AC, ModelName=model_name)
            context = {
                'test': test_record,
                'model': models,
                'TestProtocol': Test_protocol,
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
            cover_context = {
                'MNF_detail': MNF_detail,
            }
            pdf_list.insert(0, BytesIO(render_cover_to_pdf('pdf_cover.html', cover_context, request)))
            context_list = [[a, b] for a, b in zip(test_name_list, cumul_page_count_list)]
            pdf_list.insert(1, BytesIO(render_contents_to_pdf('pdf_contents.html', {'list': context_list}, request)))
        merged_pdf = merge_pdfs(pdf_list)
        response = HttpResponse(merged_pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{test_record.ModelName}_{test_record.TestStage}.pdf"'
        return response

    return HttpResponse("Invalid request method.", status=405)


def view(request, test_name, model_name, serialno):
    # Fetch the specific Test_core_detail object related to the cooling test
    Test_protocol = get_object_or_404(Test_core_detail, TestName=test_name)
    models = get_object_or_404(AC, ModelName=model_name)
    test_record = get_object_or_404(TestRecord, SerailNo=serialno)
    context = {
        'TestProtocol': Test_protocol,
        'model': models,
        'test': test_record,
    }
    return render(request, "view_test_record.html", context)

def owner_view(request, test_name, model_name, serialno):
    # Fetch the specific Test_core_detail object related to the cooling test
    Test_protocol = get_object_or_404(Test_core_detail, TestName=test_name)
    models = get_object_or_404(AC, ModelName=model_name)
    test_record = get_object_or_404(TestRecord, SerailNo=serialno)

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

def MNF(request):
    if request.method == 'POST':
        # Get form data from the request
        customer = request.POST.get('Customer')
        manufature = request.POST.get('Manufature')
        location = request.POST.get('Location')
        brand = request.POST.get('Brand')
        product = request.POST.get('prod')
        # print(product)
        brand_model_no = request.POST.get('Brand_model_no')
        Indkal_model_no = request.POST.get('Indkal_model_no')
        ORM_model_no = request.POST.get('ORM_model_no')
     

        # Create and save a new AC object
        new_mnf = Model_MNF_detail(
           Customer = customer,
           Manufature = manufature,
           Location = location,
           Brand = brand,
           Product = product,
           Brand_model_no = brand_model_no,
           Indkal_model_no = Indkal_model_no,
           ORM_model_no = ORM_model_no

        )
        new_mnf.save()
        # Redirect to a success page or render a success message
        # return redirect('/check/')  # Assuming you have a 'success' URL
        if product == 'ac':
            return render(request, 'AC.html', {'Indkal_model_no': Indkal_model_no})
       
    # If not a POST request, render the form
    return render(request, 'productMNFdetail.html')

def Test_list_entry(request):
    if request.method == 'POST':
        # Get form data from the request
        testStages = request.POST.getlist('TestStage')  # Get a list of selected test stages
        product = request.POST.get('Product')
        testName = request.POST.get('TestName')

        # Create and save the new TestList instance
        # s1 = "0000"

        # Check if a test with the same name already exists
        existing_test = TestList.objects.filter(TestName=testName, Product=product).first()
        # if existing_test:
            # s1 = existing_test.TestStage
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
        else:
            new_test = TestList(
                TestStage=s1,
                Product=product,
                TestName=testName,
            )
            new_test.save()

        # Redirect based on the existence of the test name
        if existing_test:
            messages.success(request, "Test info updated!")
            return redirect('/check/')
        else:
            return redirect('/test_protocol_entry/')

    # If not a POST request, render the form
    return render(request, 'Test_list_entry.html')

def test_protocol_entry(request):
    if request.method == 'POST':
        # Get form data from the request
        testName = request.POST.get('TestName')
        testobjective = request.POST.get('Testobjective')
        teststandard = request.POST.get('Teststandard')
        testcondition = request.POST.get('Testcondition')
        testprocedure = request.POST.get('Testprocedure')
        judgement = request.POST.get('judgement')
        instrument = request.POST.get('instrument')

        # Check if the test detail info already exists
        if Test_core_detail.objects.filter(TestName=testName).exists():
            # Display an error message if the test detail info already exists
            messages.error(request, 'Test detail info already exists')
            return redirect('/test_protocol_entry/')  # Assuming you have a 'check' URL

        # Create and save the new Test_core_detail instance
        test_detail = Test_core_detail(
            TestName=testName,
            Test_Objective=testobjective,
            Test_Standard=teststandard,
            Test_Condition=testcondition,
            Test_Procedure=testprocedure,
            Judgement=judgement,
            Instrument=instrument,
        )
        test_detail.save()

        # Redirect to a success page or render a success message
        return redirect('/check/')  # Assuming you have a 'check' URL

    # If not a POST request, render the form
    return render(request, 'test_protocol_entry.html')

def view_test_records(request):
    test_records = TestRecord.objects.all()
    return render(request, 'view.html', {'test_records': test_records})
