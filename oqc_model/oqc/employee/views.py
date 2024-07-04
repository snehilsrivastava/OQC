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
from datetime import date
from django.db.models import Q

def main_page(request):
    return redirect(login_page)

def redirect_dashboard(request):
    if request.method == 'POST':
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

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
    test_name = TestObjectRemark.TestName
    model_name = TestObjectRemark.ModelName
    serialno = TestObjectRemark.SerailNo
    if request.method == 'POST':
       
        if 'employee-remark' in request.POST:
            TestObjectRemark.employee_remark = request.POST.get('employee-remark')
        TestObjectRemark.save()
        return redirect(reverse('view', args=[test_name, model_name, serialno])) # Adjust this to your actual view name

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
            test_record.test_end_date = date.today()
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
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    # Filter the TestRecord queryset based on the parameters
    completed_tests = TestRecord.objects.all()
    completed_tests = completed_tests.filter(Q(status=1)|Q(status=2)|Q(status=3))
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

    return render(request, 'dashboard_employee.html', context)

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

            form.save()
        else:
            print(form.errors)

        messages.success(request, 'Test record updated.')
        return redirect('/check/')
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

def generate_pdf_for_legal(request,model_name,test_stage):
    if request.method == 'GET':

        selected_test_records = TestRecord.objects.filter(ModelName=model_name, TestStage=test_stage)
        if not selected_test_records.exists():
            raise Http404("No test records found")
        pdf_list = []

     
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
            # html_content = loader.render_to_string('view_pdf.html', context)
            pdf_content = render_to_pdf('view_pdf.html', context, request)
            pdf_list.append(BytesIO(pdf_content))

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


def change_status(request, test_id, status):
    test = get_object_or_404(TestRecord, id=test_id)
    test.status = status
    test.save()
    test_name = test.TestName
    model_name = test.ModelName
    serialno = test.SerailNo

        # Redirect to the owner_view page with the retrieved parameters
    return redirect('owner_view', test_name=test_name, model_name=model_name, serialno=serialno)

from django.shortcuts import get_object_or_404, redirect
from .models import TestRecord

def change_status_legal(request, test_id, status):
    test = get_object_or_404(TestRecord, id=test_id)

    if status == 1:
        test.legal_status = "Waiting for Approval"
    elif status == 2:
        test.legal_status = "Approved"
    else:
        test.legal_status = "Rejected"

    test.save()

    # Retrieve parameters for redirection
    test_name = test.TestName
    model_name = test.ModelName
    serialno = test.SerailNo

    # Redirect to legal_view with the retrieved parameters
    return redirect('legal_view', test_name=test_name, model_name=model_name, serialno=serialno)

def legal_dashboard(request):
    # Assuming 'username' is stored in the session, retrieve it
    username = request.session.get('username')

    # Retrieve distinct combinations of 'Product' and 'TestStage' from TestList model
    test = list(TestRecord.objects.values('ProductType','ModelName', 'TestStage').distinct())

    # Retrieve employee details based on 'username'
    employee = Employee.objects.get(username=username)
    all_tests = TestRecord.objects.all()
    all_tests = all_tests.order_by('-test_end_date')
    # Create an icon based on employee's first and last name initials
    icon = employee.first_name[0] + employee.last_name[0]

    # Prepare context data to pass to the template
    context = {
        'tests': test,
        'first_name': employee.first_name,
        'last_name': employee.last_name,
        'icon': icon,
        'username': username,
        'all_tests': all_tests,
    }

    # Render the template 'legal_dashboard.html' with the context data
    return render(request, "legal_dashboard.html", context)



def legal_view(request, test_name, model_name, serialno):
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
    return render(request, "legal_view.html", context)

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
            return redirect(reverse('test_protocol_entry', args=[testName, product]))

    # If not a POST request, render the form
    return render(request, 'Test_list_entry.html')

def test_protocol_entry(request,test_name,product):
    if request.method == 'POST':
        testobjective = request.POST.get('Testobjective')
        teststandard = request.POST.get('Teststandard')
        testcondition = request.POST.get('Testcondition')
        testprocedure = request.POST.get('Testprocedure')
        judgement = request.POST.get('judgement')
        instrument = request.POST.get('instrument')

        # Check if the test detail info already exists
        if Test_core_detail.objects.filter(TestName=test_name ,  ProductType = product).exists():
            # Display an error message if the test detail info already exists
            existing_test = Test_core_detail.objects.filter(TestName=test_name, Product=product).first()
            existing_test.Test_Objective=testobjective,
            existing_test.Test_Standard=teststandard,
            existing_test.Test_Condition=testcondition,
            existing_test.Test_Procedure=testprocedure,
            existing_test.Judgement=judgement,
            existing_test.Instrument=instrument,
            existing_test.save()
            return redirect('/check/')  

        # Create and save the new Test_core_detail instance
        test_detail = Test_core_detail(
            ProductType = product,
            TestName=test_name,
            Test_Objective=testobjective,
            Test_Standard=teststandard,
            Test_Condition=testcondition,
            Test_Procedure=testprocedure,
            Judgement=judgement,
            Instrument=instrument,
        )
        test_detail.save()

        # Redirect to a success page or render a success message
        return redirect('/dashboard/')  # Assuming you have a 'check' URL

    # If not a POST request, render the form
    return render(request, 'test_protocol_entry.html', {'test_name': test_name, 'product': product})

def update_test_list_entry(request):
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
       

        # messages.success(request, "Test info updated!")

        return redirect(reverse('test_protocol_entry', args=[testName, product]))

    test_names = TestList.objects.values_list('TestName', flat=True).distinct()
    products = Product_Detail.objects.values_list('ProductType', flat=True).distinct()
    
    context = {
        'test_names': test_names,
        'products': products,
    }
    
    return render(request, 'Update_Test_list_entry.html', context)



def view_test_records(request):
    test_records = TestRecord.objects.all()
    return render(request, 'view.html', {'test_records': test_records})
