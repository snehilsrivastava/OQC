from django.shortcuts import render,redirect
from .models import *
from employee.models import TestRecord, Test_core_detail
from django.urls import reverse
from authapp.models import Employee
from django.contrib import messages

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
        return redirect(reverse('report', kwargs={'test_name': test_name, 'model_name': model_name, 'serialno': serial_no}))

    tv_models = list(TV.objects.values_list('ModelName', flat=True).distinct())
    ac_models = list(AC.objects.values_list('ModelName', flat=True).distinct())
    phone_models = list(Phone.objects.values_list('ModelName', flat=True).distinct())
    washing_machine_models = list(WM_FATL.objects.values_list('ModelName', flat=True).distinct())
    test = list(Test_core_detail.objects.values('ProductType', 'TestStage', 'TestName'))
    products = list(Test_core_detail.objects.values_list('ProductType', flat=True).distinct())
    context = {
        'tv_models': tv_models,
        'ac_models': ac_models,
        'phone_models': phone_models,
        'washing_machine_models': washing_machine_models,
        'test': test,
        'products': products,
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
        existing_AC = AC.objects.filter(ModelName=model_name)
        if not existing_AC:
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
        test_names = Product_Test_Name_Details.objects.get(Product="AC").Test_Names
        dvt = test_names['DVT']
        pp = test_names['PP']
        mp = test_names['MP']
        context = {
            'model_name': model_name,
            'product': "AC",
            'DVT': dvt,
            'PP': pp,
            'MP': mp,
        }
        return render(request, 'TestNames.html', context)
    messages.error(request, 'Invalid request')
    return redirect('/dashboard/')

@login_required
def WM_FATL_spec(request):
    user = Employee.objects.get(username=request.session['username'])
    if user.user_type != 'owner' and not user.is_superuser:
        return redirect('/access_denied/')
    if request.method == 'POST':
        model_name = request.POST.get('ModelName')
        rated_capacity = request.POST.get('RatedCapacity')
        rated_power = request.POST.get('RatedPower')
        rated_supply = request.POST.get('RatedSupply')
        rated_frequency = request.POST.get('RatedFrequency')
        rated_rpm = request.POST.get('RatedRPM')
        existing_WM_FATL = WM_FATL.objects.filter(ModelName=model_name)
        if not existing_WM_FATL:
            new_WM_FATL = WM_FATL(
                ModelName=model_name,
                RatedCapacity = rated_capacity,
                RatedPower = rated_power,
                RatedSupply = rated_supply,
                RatedFrequency = rated_frequency,
                RatedRPM = rated_rpm,
            )
            new_WM_FATL.save()
        test_names = Product_Test_Name_Details.objects.get(Product="WM - FATL").Test_Names
        dvt = test_names['DVT']
        pp = test_names['PP']
        mp = test_names['MP']
        context = {
            'model_name': model_name,
            'product': "WM - FATL",
            'DVT': dvt,
            'PP': pp,
            'MP': mp,
        }
        return render(request, 'TestNames.html', context)
    messages.error(request, 'Invalid request')
    return redirect('/dashboard/')

@login_required
def TestNames(request):
    user = Employee.objects.get(username=request.session['username'])
    if user.user_type != 'owner' and not user.is_superuser:
        return redirect('/access_denied/')
    if request.method == 'POST':
        model_name = request.POST.get('ModelName')
        product = request.POST.get('Product')
        dvt = request.POST.getlist('dvt-options')
        pp = request.POST.getlist('pp-options')
        mp = request.POST.getlist('mp-options')
        model_test_names = {"DVT": dvt, "PP": pp, "MP": mp}
        new_model_test_name_details = Model_Test_Name_Details(
            Model_Name=Model_MNF_detail.objects.get(Indkal_model_no=model_name),
            Test_Names=model_test_names
        )
        new_model_test_name_details.save()
        messages.success(request, 'Model saved')
        return redirect('/dashboard/')
    messages.error(request, 'Invalid request')
    return redirect('/dashboard/')