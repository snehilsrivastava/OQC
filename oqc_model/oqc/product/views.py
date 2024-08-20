from django.shortcuts import render,redirect
from .models import *
from employee.models import TestRecord, Test_core_detail
from django.shortcuts import render
from .models import TV, AC, Phone, Washing_Machine
from django.urls import reverse
from authapp.models import Employee

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        next_page = request.original_path
        if 'username' in request.session:
            return view_func(request, *args, **kwargs)
        login_url = '/au/login'
        return redirect(f"{login_url}?next={next_page}" if next_page else login_url)
    return wrapper

@login_required
def product_form_view(request):
    user = Employee.objects.get(username=request.session['username'])
    if (user.user_type != 'employee' and user.user_type != 'owner') and not user.is_superuser:
        return redirect('/access_denied/')
    if request.method == 'POST':
        product_type = request.POST.get('ProductType')
        model_name = request.POST.get('ModelName')
        test_stage = request.POST.get('TestStage')
        test_name = request.POST.get('TestName')
        serial_no = request.POST.get('SerailNo')
        tested_by = request.POST.get('TestedBy')
        username = request.session['username']
        employee = Employee.objects.get(username=username)
        name = employee.first_name + ' ' + employee.last_name
        new_product_detail = TestRecord(
            ProductType=product_type,
            ModelName=model_name,
            SerailNo=serial_no,
            TestStage=test_stage,
            TestName=test_name,
            employee=username,
            employee_name=name,
            status = "Approved" if user.user_type == "owner" else "Not Sent",
            verification = True if tested_by == 'ODM' else False,
        )
        new_product_detail.save()
        return redirect(reverse('cooling', kwargs={'test_name': test_name, 'model_name': model_name, 'serialno': serial_no}))

    tv_models = list(TV.objects.values_list('ModelName', flat=True))
    ac_models = list(AC.objects.values_list('ModelName', flat=True))
    phone_models = list(Phone.objects.values_list('ModelName', flat=True))
    washing_machine_models = list(WM_FATL.objects.values_list('ModelName', flat=True))
    user = request.session['username']
    test = list(Test_core_detail.objects.values('ProductType', 'TestStage', 'TestName'))
    username = request.session['username']
    employee = Employee.objects.get(username=username)
    icon = employee.first_name[0] + employee.last_name[0]
    context = {
        'tv_models': tv_models,
        'ac_models': ac_models,
        'phone_models': phone_models,
        'washing_machine_models': washing_machine_models,
        'user': user,
        'test': test,
        'first_name': employee.first_name,
        'last_name': employee.last_name,
        'icon': icon,
        'username': username,
    }
    return render(request, 'product.html', context)

@login_required
def AC_spec(request):
    user = Employee.objects.get(username=request.session['username'])
    if user.user_type != 'owner' and not user.is_superuser:
        return redirect('/access_denied/')
    if request.method == 'POST':
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
        return redirect('/dashboard/')

    username = request.session['username']
    employee = Employee.objects.get(username=username)
    icon = employee.first_name[0] + employee.last_name[0]
    context = {
        'first_name': employee.first_name,
        'last_name': employee.last_name,
        'icon': icon,
        'username': username,
    }
    return render(request, 'AC.html', context=context)