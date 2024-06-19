from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.core.files import File
from django.conf import settings
from django.http import Http404
from .forms import *
from .models import *
from .renderers import *
from product.views import *
from authapp.models import Employee
from authapp.views import login_page
import PyPDF2
import base64
from tempfile import NamedTemporaryFile
from io import BytesIO
from django.contrib import messages


def main_page(request):
    return redirect(login_page)

def members(request):
  mymembers = Employee.objects.all().values()
  template = loader.get_template('check.html')
  context = {
    'mymembers': mymembers,
  }
  return HttpResponse(template.render(context, request))

from django.shortcuts import render, get_object_or_404

def testdetail(request, no):
    if request.method == 'GET':
        context = {
            'report': get_object_or_404(Test, no=no),
            'bill_base': "bill_base.html",
       
        }
        return render(request, "test1.html", context)
    
    elif request.method == 'POST':
        no = request.POST.get('no')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        # Process the POST data as needed
        context = {
            'report': get_object_or_404(Test, no=no),
            'bill_base': "bill_base.html",
            'start_date': start_date,
            'end_date': end_date,
        }
        return render(request, "test1.html", context)


# def check(request):
#     username = request.session.get('username')
    
#     if username is None:
#         return redirect('login')  # Redirect to login page if username is not in session

#     # Fetch all test records associated with the username
#     completed_tests = TestRecord.objects.filter(employee=username)

#     context = {
#        'completed_tests': completed_tests
#     }

#     return render(request, "test_report.html", context)

from django.shortcuts import render
from .models import TestRecord

def check(request):
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
    completed_tests = TestRecord.objects.filter(employee=username)

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
    }

    return render(request, "test_report.html", context)




def cooling(request, test_name, model_name, serialno):
    # Fetch the specific Test_core_detail object related to the cooling test
    Test_protocol = get_object_or_404(Test_core_detail, TestName=test_name)
    models = get_object_or_404(AC, ModelName=model_name)
    test_record = get_object_or_404(TestRecord, SerailNo=serialno)

    if request.method == 'POST':
        form = TestRecordForm(request.POST, instance=test_record)  
        if form.is_valid():
            print("random")
            form.save()
        else:
            print(form.errors)
       
        return redirect('/check/')  # Redirect to a success page or another view
    else:
        form = TestRecordForm(instance=test_record)

    # if request.method == 'POST':
    #     form = testItemFormset(request.POST)
    #     if form.is_valid():
    #         # Update the test record with form data
    #         test_record.sample_quantiy = form.cleaned_data.get("quantiy")
    #         test_record.test_date = form.cleaned_data.get("ReportDate")
    #         test_record.test_start_date = form.cleaned_data.get("StartDate")
    #         test_record.test_end_date = form.cleaned_data.get("EndDate")
    #         test_record.result = form.cleaned_data.get("Result")
    #         test_record.notes = form.cleaned_data.get("Notes")
    #         test_record.save()

    #     return redirect('/check/')  # Redirect to a success page or another view
    # else:
    #     form = testItemFormset()

    # Pass the data to the template
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


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import TestRecord

@csrf_exempt
def toggle_status(request, id):
    if request.method == 'POST':
        test_record = get_object_or_404(TestRecord, id=id)
        test_record.status = not test_record.status
        test_record.save()
        return JsonResponse({'success': True, 'new_status': test_record.status})
    return JsonResponse({'success': False})



def view_test_report(request,pk):
    record = get_object_or_404(TestRecord, pk =pk)
    images = record.images.all()  # Fetch all images related to this record
    return render(request, 'view_record.html', {'record': record, 'images': images})

def dashboard(request):
    users = Employee.objects.all()
    context = {
        'users': users
    }
    return render(request, 'dashboard_employee.html', context)
            
def logout(request):
    if request.method == "POST":
        # logout(request)
        context = {
            'success_message': "You have successfully logged out."
        }
        return render(request, 'logout.html', context)
    return render(request, 'logout.html')

def submit_product_details_view(request):
    return HttpResponse("Thank you for submitting product details")

@login_required
def create_test_record(request):
    if request.method == 'POST':
        num_images = int(request.POST.get('num_images', 0))  # Default to 0 images
        print(f"Number of images: {num_images}")
        
        TestImageFormSet = modelformset_factory(TestImage, form=TestImageForm, extra=num_images)
        report_form = TestRecordForm(request.POST)
        formset = TestImageFormSet(request.POST, request.FILES, queryset=TestImage.objects.none())

        if report_form.is_valid() and formset.is_valid():
            # First, save the TestRecord instance
            report = report_form.save(commit=False)
            report.employee = Employee.objects.get(username=request.user.username)
            report.save()

            # Next, save the formset images and associate them with the report
            for form in formset:
                if form.cleaned_data:  # Ensure the form has data
                    image_instance = form.save(commit=False)
                    image_instance.report = report
                    image_instance.save()

            # Handle captured images
            for i in range(num_images):
                print(f"Processing image {i}")
                captured_image_data = request.POST.get(f'captured_images_{i}')
                print(f"Captured image data for {i}: {captured_image_data}")
                if captured_image_data:
                    # Extract image data from base64 string
                    format, imgstr = captured_image_data.split(';base64,')
                    ext = format.split('/')[-1]
                    # Decode base64 data
                    data = base64.b64decode(imgstr)

                    # Create a temporary file to hold the image data
                    temp_image = NamedTemporaryFile(delete=True)
                    temp_image.write(data)
                    temp_image.flush()

                    # Create a Django File object from the temporary file
                    image = File(temp_image, name=f'captured_image_{i}.{ext}')

                    # Create and save TestImage object with the report and image
                    TestImage.objects.create(report=report, image=image)

            return redirect('view')  # Replace 'view' with your actual view name or URL name
        else:
            # Debug statements to understand form errors
            print("Report form errors:", report_form.errors)
            print("Formset errors:", formset.errors)
    else:
        num_images = 0  # Default to 0 images
        if 'num_images' in request.GET:
            num_images = int(request.GET.get('num_images'))
        TestImageFormSet = modelformset_factory(TestImage, form=TestImageForm, extra=num_images)

        report_form = TestRecordForm()
        formset = TestImageFormSet(queryset=TestImage.objects.none())

    return render(request, 'create_test_record.html', {
        'report_form': report_form,
        'formset': formset,
        'num_images': num_images
    })


@login_required
def edit_test_record(request, pk):
    test_record = get_object_or_404(TestRecord, pk=pk)
    
    if request.method == 'POST':
        form = TestRecordForm(request.POST, instance=test_record)
        if form.is_valid():
            form.save()
            return redirect('view')
    else:
        form = TestRecordForm(instance=test_record)
    return render(request, 'edit_test_record.html', {'form': form})

def merge_pdfs(pdf_files):
    merger = PyPDF2.PdfMerger()
    for pdf_file in pdf_files:
        pdf_buffer = BytesIO(pdf_file)
        merger.append(pdf_buffer)
    merged_pdf = BytesIO()
    merger.write(merged_pdf)
    merger.close()
    return merged_pdf.getvalue()

def generate_pdf(request):
    if request.method == 'POST':
        selected_test_ids = request.POST.getlist('selected_tests')

        # Retrieve the selected test records from the database
        selected_test_records = TestRecord.objects.filter(pk__in=selected_test_ids)
        if not selected_test_records.exists():
            raise Http404("No test records found")

        pdf_files = []

        for i, test_record in enumerate(selected_test_records, start=1):
            record_data = {
                'date': test_record.test_date,
                'name': test_record.test_name,
                'no': i,
                'result': test_record.result,
                'notes': test_record.notes,
                'images': TestImage.objects.filter(report=test_record),
                'MEDIA_URL': settings.MEDIA_URL  # Add MEDIA_URL to context
            }

            if test_record.test_name == 'Test1':
                pdf = render_to_pdf('view_test_record.html', {'record': record_data})
            elif test_record.test_name == 'Test2':
                pdf = render_to_pdf('view_test_record.html', {'record': record_data})
            else:
                pdf = render_to_pdf('home.html', {'record': record_data})
            
            if pdf:
                pdf_files.append(pdf)


        if pdf_files:
            merged_pdf = merge_pdfs(pdf_files)
            response = HttpResponse(merged_pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="test_records.pdf"'
            return response
        else:
            return HttpResponse("No PDF files generated.", status=500)

    return HttpResponse("Invalid request method.", status=405)

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
        # Update s1 based on the selected test stages
        # for stage in testStages:
        #     if stage == "DVT":
        #         s1 = '1' + s1[1:]
        #     elif stage == "PP":
        #         s1 = s1[0] + '1' + s1[2:]
        #     elif stage == "MP":
        #         s1 = s1[:2] + '1' + s1[3:]
        #     elif stage == "PDI":
        #         s1 = s1[:3] + '1'

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


