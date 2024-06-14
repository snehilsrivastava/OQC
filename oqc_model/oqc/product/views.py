from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
from authapp.models import Employee
from employee.models import TestList


from django.shortcuts import render, HttpResponse
from .models import Product_Detail, TV, AC, Phone, Washing_Machine
from django.urls import reverse

def product_form_view(request):
    if request.method == 'POST':
        product_type = request.POST.get('ProductType')
        model_name = request.POST.get('ModelName')
        serial_no = request.POST.get('SerailNo')
        test_stage = request.POST.get('TestStage')
        test_name = request.POST.get('TestName')

        # Check if the serial number already exists in the database
        if Product_Detail.objects.filter(SerailNo=serial_no).exists():
            return HttpResponse("Serial number already exists")

        # Generate the 'no' field based on the existing entries
        last_product = Product_Detail.objects.last()
        if last_product:
            no = last_product.no + 1
        else:
            no = 1

        print(no)

        # Create and save the new Product_Detail instance
        new_product_detail = Product_Detail(
            no=no,
            ProductType=product_type,
            ModelName=model_name,
            SerailNo=serial_no,
            TestStage = test_stage,
            TestName = test_name
        )
        new_product_detail.save()

        return redirect(reverse('cooling', kwargs={'test_name': test_name, 'model_name': model_name}))



    # If GET request, prepare context with models data
    tv_models = list(TV.objects.values_list('ModelName', flat=True))
    ac_models = list(AC.objects.values_list('ModelName', flat=True))
    phone_models = list(Phone.objects.values_list('ModelName', flat=True))
    washing_machine_models = list(Washing_Machine.objects.values_list('ModelName', flat=True))
    users = Employee.objects.all()
    test = list(TestList.objects.all().values())
 
    
    context = {
        'tv_models': tv_models,
        'ac_models': ac_models,
        'phone_models': phone_models,
        'washing_machine_models': washing_machine_models,
        'users': users,
        'test' : test
    }
    
    return render(request, 'product.html', context)

def AC_spec(request):
    
    if request.method == 'POST':
        # Get form data from the request
        model_name = request.POST.get('ModelName')
        bi_motor = request.POST.get('BImotor')
        blower = request.POST.get('Blower')
        fan_motor = request.POST.get('FanMotor')
        eva = request.POST.get('Eva')
        fan = request.POST.get('Fan')
        con_pipe = request.POST.get('ConPipe')
        cond_coil = request.POST.get('CondCoil')
        ref_charge = request.POST.get('RefCharge')
        capilary = request.POST.get('Capilary')
        compressor = request.POST.get('Compressor') 

        # Create and save a new AC object
        new_ac = AC(
            ModelName=model_name,
            BImotor=bi_motor,
            Blower=blower,
            FanMotor=fan_motor,
            Eva=eva,
            Fan=fan,
            ConPipe=con_pipe,
            CondCoil=cond_coil,
            RefCharge=ref_charge,
            Capilary=capilary,
            Compressor=compressor
        )
        new_ac.save()

        # Redirect to a success page or render a success message
        return redirect('/check/')  # Assuming you have a 'success' URL

    # If not a POST request, render the form
    return render(request, 'AC.html')








