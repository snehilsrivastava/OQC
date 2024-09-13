from django.shortcuts import render,redirect
from .models import *
from employee.models import TestRecord, Test_core_detail
from django.urls import reverse
from authapp.models import Employee, Notification, default_notification
from django.contrib import messages
import json
from datetime import datetime as dt

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
        new_product_detail = TestRecord(
            ProductType=product_type,
            ModelName=model_name,
            SerailNo=serial_no,
            TestStage=test_stage,
            TestName=test_name,
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
def specs(request, model, product):
    user = Employee.objects.get(username=request.session['username'])
    user_PT = [PT for PT in user.product_type if user.product_type[PT]]
    if (user.user_type != 'owner' and not user.is_superuser) or product not in user_PT:
        return redirect('/access_denied/')
    
    context = {'product': product, 'model': model}
    if product == 'AC':
        context['AC_model'] = AC.objects.get(ModelName=model)
    elif product == 'WM - FATL':
        context['WM_model'] = WM_FATL.objects.get(ModelName=model)
    return render(request, 'specs.html', context)

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
        else:
            existing_AC.update(
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
        test_details = Test_core_detail.objects.filter(ProductType="AC")
        test_names = test_details.values_list('TestName', flat=True)
        test_stages = test_details.values_list('TestStage', flat=True)
        dvt, pp, mp = [], [], []
        for i, stage in enumerate(test_stages):
            if int(stage[0]):
                dvt.append(test_names[i])
            if int(stage[1]):
                pp.append(test_names[i])
            if int(stage[2]):
                mp.append(test_names[i])
        selected_dvt, selected_pp, selected_mp = [0 for _ in dvt], [0 for _ in pp], [0 for _ in mp]
        timeline = {'DVT': [], 'PP': [], 'MP': []}
        if Model_Test_Name_Details.objects.filter(Model_Name=model_name).exists():
            _dvt = list(Model_Test_Name_Details.objects.get(Model_Name=model_name).Test_Names['DVT'])
            _pp = list(Model_Test_Name_Details.objects.get(Model_Name=model_name).Test_Names['PP'])
            _mp = list(Model_Test_Name_Details.objects.get(Model_Name=model_name).Test_Names['MP'])
            for i in range(len(dvt)):
                selected_dvt[i] = 1 if dvt[i] in _dvt else 0
            for i in range(len(pp)):
                selected_pp[i] = 1 if pp[i] in _pp else 0
            for i in range(len(mp)):
                selected_mp[i] = 1 if mp[i] in _mp else 0
            timeline['DVT'] = list(Model_Test_Name_Details.objects.get(Model_Name=model_name).Time_Line['DVT'])
            timeline['PP'] = list(Model_Test_Name_Details.objects.get(Model_Name=model_name).Time_Line['PP'])
            timeline['MP'] = list(Model_Test_Name_Details.objects.get(Model_Name=model_name).Time_Line['MP'])
        context = {
            'model_name': model_name,
            'product': "AC",
            'DVT': dvt,
            'PP': pp,
            'MP': mp,
            'selected_dvt': selected_dvt,
            'selected_pp': selected_pp,
            'selected_mp': selected_mp,
            'timeline_dvt': timeline['DVT'],
            'timeline_pp': timeline['PP'],
            'timeline_mp': timeline['MP'],
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
        else:
            existing_WM_FATL.update(
                RatedCapacity = rated_capacity,
                RatedPower = rated_power,
                RatedSupply = rated_supply,
                RatedFrequency = rated_frequency,
                RatedRPM = rated_rpm,
            )
        test_details = Test_core_detail.objects.filter(ProductType="WM - FATL")
        test_names = test_details.values_list('TestName', flat=True)
        test_stages = test_details.values_list('TestStage', flat=True)
        dvt, pp, mp = [], [], []
        for i, stage in enumerate(test_stages):
            if int(stage[0]):
                dvt.append(test_names[i])
            if int(stage[1]):
                pp.append(test_names[i])
            if int(stage[2]):
                mp.append(test_names[i])
        selected_dvt, selected_pp, selected_mp = [0 for _ in dvt], [0 for _ in pp], [0 for _ in mp]
        timeline = {'DVT': [], 'PP': [], 'MP': []}
        if Model_Test_Name_Details.objects.filter(Model_Name=model_name).exists():
            _dvt = list(Model_Test_Name_Details.objects.get(Model_Name=model_name).Test_Names['DVT'])
            _pp = list(Model_Test_Name_Details.objects.get(Model_Name=model_name).Test_Names['PP'])
            _mp = list(Model_Test_Name_Details.objects.get(Model_Name=model_name).Test_Names['MP'])
            for i in range(len(dvt)):
                selected_dvt[i] = 1 if dvt[i] in _dvt else 0
            for i in range(len(pp)):
                selected_pp[i] = 1 if pp[i] in _pp else 0
            for i in range(len(mp)):
                selected_mp[i] = 1 if mp[i] in _mp else 0
            timeline['DVT'] = list(Model_Test_Name_Details.objects.get(Model_Name=model_name).Time_Line['DVT'])
            timeline['PP'] = list(Model_Test_Name_Details.objects.get(Model_Name=model_name).Time_Line['PP'])
            timeline['MP'] = list(Model_Test_Name_Details.objects.get(Model_Name=model_name).Time_Line['MP'])
            for stage in timeline:
                for i in [0, 1]:
                    if timeline[stage][i] != '':
                        timeline[stage][i] = dt.strptime(timeline[stage][i], '%d/%m/%Y').strftime('%Y-%m-%d')
        context = {
            'model_name': model_name,
            'product': "WM - FATL",
            'DVT': dvt,
            'PP': pp,
            'MP': mp,
            'selected_dvt': selected_dvt,
            'selected_pp': selected_pp,
            'selected_mp': selected_mp,
            'timeline_dvt': timeline['DVT'],
            'timeline_pp': timeline['PP'],
            'timeline_mp': timeline['MP'],
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
        print("=======================\n",dvt, pp, mp, "\n========================")
        tl = {'DVT': ['NA', 'NA'], 'PP': ['NA', 'NA'], 'MP': ['NA', 'NA']}
        tl['DVT'][0] = request.POST.get('dvt-start-date')
        tl['DVT'][1] = request.POST.get('dvt-end-date')
        tl['PP'][0] = request.POST.get('pp-start-date')
        tl['PP'][1] = request.POST.get('pp-end-date')
        tl['MP'][0] = request.POST.get('mp-start-date')
        tl['MP'][1] = request.POST.get('mp-end-date')
        for stage in tl:
            for i in [0, 1]:
                if tl[stage][i] !='':
                    tl[stage][i] = dt.strptime(tl[stage][i], '%Y-%m-%d').strftime('%d/%m/%Y')
        model_test_names = {"DVT": dvt, "PP": pp, "MP": mp}
        model_updated = False
        if Model_Test_Name_Details.objects.filter(Model_Name=model_name).exists():
            existing_model_test_name_details = Model_Test_Name_Details.objects.get(Model_Name=model_name)
            existing_model_test_name_details.Test_Names = model_test_names
            existing_model_test_name_details.Time_Line = {"DVT": [tl['DVT'][0], tl['DVT'][1]], "PP": [tl['PP'][0], tl['PP'][1]], "MP": [tl['MP'][0], tl['MP'][1]]}
            existing_model_test_name_details.save()
            delete_reports(request, model_name)
            model_updated = True
        else:
            new_model_test_name_details = Model_Test_Name_Details(
                Model_Name=Model_MNF_detail.objects.get(Indkal_model_no=model_name),
                Test_Names=model_test_names,
                Time_Line = tl
            )
            new_model_test_name_details.save()
        generate_reports(request, model_name, model_updated)
        messages.success(request, 'Model saved')
        return redirect('/dashboard/')
    messages.error(request, 'Invalid request')
    return redirect('/dashboard/')

@login_required
def generate_reports(request, model_name, model_updated):
    model = Model_Test_Name_Details.objects.get(Model_Name = Model_MNF_detail.objects.get(Indkal_model_no = model_name))
    model_tests = model.Test_Names
    model_product = model.Product
    created_reports = 0
    for stage, test_names in model_tests.items():
        for test_name in test_names:
            if not TestRecord.objects.filter(ProductType=model_product, ModelName=model_name, TestStage=stage, TestName=test_name).exists():
                test_record = TestRecord.objects.create(
                    ProductType=model_product,
                    ModelName=model_name,
                    TestName=test_name,
                    TestStage=stage,
                )
                test_record.save()
                created_reports += 1
    # send notification to owners and employees
    user = Employee.objects.get(username=request.session['username'])
    if created_reports > 0:
        employees = Employee.objects.filter(user_type__in=['employee', 'owner'])
        for employee in employees:
            user_ProdType = [k for k in employee.product_type if employee.product_type[k]]
            if model_product in user_ProdType:
                notification = Notification.objects.get(employee=employee.username)
                notification_dict = default_notification()
                notification_dict["from"] = f"{user.first_name} {user.last_name}"
                if model_updated:
                    notification_dict["display_content"] = f"{user.first_name} {user.last_name} updated model: {model_name}"
                    notification_dict["display_full_content"] = f"Updated model {model_name} and created {created_reports} reports for product: {model_product}."
                else:
                    notification_dict["display_content"] = f"{user.first_name} {user.last_name} added model: {model_name}"
                    notification_dict["display_full_content"] = f"Added model {model_name} and created {created_reports} reports for product: {model_product}."
                notification_dict["metadata"] = {
                    "product": model_product,
                    "model": model_name
                }
                notification_dict["action"] = "created"
                notif_dict = json.dumps(notification_dict)
                notification.notification.append(notif_dict)
                notification.unread_count += 1
                notification.save()

@login_required
def delete_reports(request, model_name):
    model = Model_Test_Name_Details.objects.get(Model_Name = model_name)
    model_tests = model.Test_Names
    model_product = model.Product
    records = TestRecord.objects.filter(ProductType=model_product, ModelName=model_name)
    for stage, test_names in model_tests.items():
        recorded_tests = records.filter(TestStage=stage)
        for recorded_test in recorded_tests:
            if recorded_test.TestName not in test_names:
                recorded_test.delete()
