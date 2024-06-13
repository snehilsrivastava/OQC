from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from authapp.models import Employee 
from .models import *
from product.views import *
from django.contrib import messages
import io
from authapp.views import login_page

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
    
# def check(request, no):
#     if request.method == 'GET':
#         context = {
#             'report': get_object_or_404(Test, no=no),
#             'bill_base': "bill_base.html",
       
#         }
#         return render(request, "test_report.html", context)
    
#     elif request.method == 'POST':
#         no = request.POST.get('no')
#         start_date = request.POST.get('start_date')
#         end_date = request.POST.get('end_date')
#         # Process the POST data as needed
#         context = {
#             'report': get_object_or_404(Test, no=no),
#             'bill_base': "bill_base.html",
#             'start_date': start_date,
#             'end_date': end_date,
#         }
#         return render(request, "test_report.html", context)

def check(request):
    return render(request,"test_report.html")

def cooling(request):
    return render(request,"cooling_test.html")

def MNF(request):
    return render(request,"productMNFdetail.html")

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
        logout(request)
        context = {
            'success_message': "You have successfully logged out."
        }
        return render(request, 'logout.html', context)
    return render(request, 'logout.html')

def submit_product_details_view(request):
    return HttpResponse("Thank you for submitting product details")


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import TestRecord
import base64
from django.core.files.base import ContentFile
from .forms import TestRecordForm

import datetime
from django.http import HttpResponse, Http404
from employee import renderers


from django.contrib.auth.decorators import login_required
import base64
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.http import Http404
from django.forms import modelformset_factory
from .models import TestRecord, TestImage, Employee
from .forms import TestRecordForm, TestImageForm
import base64
from urllib.request import urlopen
from django.core.files.base import ContentFile
from django.core.files import File
from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from .models import TestImage, TestRecord, Employee  # Adjust import paths as needed
from .forms import TestRecordForm, TestImageForm

from tempfile import NamedTemporaryFile


from django.core.files.base import ContentFile
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import base64

from django.core.files import File


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



from django.http import HttpResponse, Http404
from .models import TestRecord
from .renderers import render_to_pdf
from PyPDF2 import PdfMerger
from io import BytesIO

import PyPDF2
from io import BytesIO
from django.conf import settings
from django.conf.urls.static import static

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
        brand_model_no = request.POST.get('Brand_model_no')
        Indkal_model_no = request.POST.get('Indkal_model_no')
        ORM_model_no = request.POST.get('ORM_model_no')
     

        # Create and save a new AC object
        new_mnf = Model_MNF_detail(
           Customer = customer,
           Manufature = manufature,
           Location = location,
           Brand = brand,
           Brand_model_no = brand_model_no,
           Indkal_model_no = Indkal_model_no,
           ORM_model_no = ORM_model_no

        )
        new_mnf.save()

        # Redirect to a success page or render a success message
        return redirect('/check/')  # Assuming you have a 'success' URL

    # If not a POST request, render the form
    return render(request, 'productMNFdetail.html')


def Test_list_entry(request):
    
    if request.method == 'POST':
        # Get form data from the request
        testStage = request.POST.get('TestStage')
        product = request.POST.get('Product')
        testName = request.POST.get('TestName')
     

        # Create and save a new AC object
        new_test = TestList(
           TestStage = testStage,
           Product = product,
           TestName = testName,
           

        )
        new_test.save()

        # Redirect to a success page or render a success message
        return redirect('/check/')  # Assuming you have a 'success' URL

    # If not a POST request, render the form
    return render(request, 'Test_list_entry.html')




def view_test_records(request):
    test_records = TestRecord.objects.all()
    return render(request, 'view.html', {'test_records': test_records})


