from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
from employee.models import TestRecord
from django.shortcuts import render, HttpResponse
from .models import Product_Detail, TV, AC, Phone, Washing_Machine
from django.urls import reverse
from employee.models import TestList
from authapp.models import Employee

def product_form_view(request):
    if request.method == 'POST':
        product_type = request.POST.get('ProductType')
        model_name = request.POST.get('ModelName')
        serial_no = request.POST.get('SerailNo')
        test_stage = request.POST.get('TestStage')
        test_name = request.POST.get('TestName')
        username = request.session['username'].strip()

        new_product_detail = TestRecord(
            ProductType=product_type,
            ModelName=model_name,
            SerailNo=serial_no,
            TestStage=test_stage,
            TestName=test_name,
            employee=username,
        )
        new_product_detail.save()
        return redirect(reverse('cooling', kwargs={'test_name': test_name, 'model_name': model_name, 'serialno': serial_no}))

    # If GET request, prepare context with models data
    tv_models = list(TV.objects.values_list('ModelName', flat=True))
    ac_models = list(AC.objects.values_list('ModelName', flat=True))
    phone_models = list(Phone.objects.values_list('ModelName', flat=True))
    washing_machine_models = list(Washing_Machine.objects.values_list('ModelName', flat=True))
    user = request.session['username']
    test = list(TestList.objects.values('Product', 'TestStage', 'TestName'))

    context = {
        'tv_models': tv_models,
        'ac_models': ac_models,
        'phone_models': phone_models,
        'washing_machine_models': washing_machine_models,
        'user': user,
        'test': test,
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
        return redirect('/dashboard/')  # Assuming you have a 'success' URL

    # If not a POST request, render the form
    username = request.session['username']
    employee = Employee.objects.get(username=username)
    icon = employee.first_name[0] + employee.last_name[0]

    context = {
        'first_name': employee.first_name,
        'last_name': employee.last_name,
        'icon': icon,
        'username': username,
    }
    return render(request, 'AC.html')