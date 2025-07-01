from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import json
import pandas as pd

from .models import PatientProfile, UrineAnalysis, SerumLabs, OxalateContent, ManagementPlan
from .forms import (
    PatientProfileForm, UrineAnalysisForm, SerumLabsForm,
    AcuteManagementForm, ManagementPlanForm, OxalateSearchForm
)
from .services import interpret_24hr_urine, generate_management_plan, get_acute_management_guidance


def home(request):
    """Home page with navigation to different sections"""
    return render(request, 'kidney_stones_app/home.html')


def patient_profile(request):
    """Patient Profile & History page"""
    if request.method == 'POST':
        form = PatientProfileForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            if request.user.is_authenticated:
                patient.user = request.user
            patient.save()
            messages.success(request, 'Patient profile saved successfully!')
            return redirect('kidney_stones_app:urine_analysis')
    else:
        form = PatientProfileForm()

    return render(request, 'kidney_stones_app/patient_profile.html', {
        'form': form,
        'active_page': 'patient_profile'
    })


def urine_analysis(request):
    """24-Hour Urine Analysis page"""
    # Get the most recent patient profile
    try:
        if request.user.is_authenticated:
            patient_profile = PatientProfile.objects.filter(
                user=request.user).latest('created_at')
        else:
            patient_profile = PatientProfile.objects.latest('created_at')
    except PatientProfile.DoesNotExist:
        messages.warning(request, 'Please complete the Patient Profile first.')
        return redirect('kidney_stones_app:patient_profile')

    if request.method == 'POST':
        urine_form = UrineAnalysisForm(request.POST)
        serum_form = SerumLabsForm(request.POST)

        if urine_form.is_valid() and serum_form.is_valid():
            urine_analysis = urine_form.save(commit=False)
            urine_analysis.patient_profile = patient_profile
            urine_analysis.save()

            serum_labs = serum_form.save(commit=False)
            serum_labs.patient_profile = patient_profile
            serum_labs.save()

            # Convert to dict for interpretation
            urine_data = {
                'volume_L': float(urine_analysis.volume_L),
                'ph': float(urine_analysis.ph),
                'calcium_mg': urine_analysis.calcium_mg,
                'oxalate_mg': urine_analysis.oxalate_mg,
                'phosphorus_mg': urine_analysis.phosphorus_mg,
                'uric_acid_mg': urine_analysis.uric_acid_mg,
                'sodium_mEq': urine_analysis.sodium_mEq,
                'potassium_mEq': urine_analysis.potassium_mEq,
                'magnesium_mg': urine_analysis.magnesium_mg,
                'sulfate_mmol': urine_analysis.sulfate_mmol,
                'ammonium_mmol': urine_analysis.ammonium_mmol,
                'citrate_mg': urine_analysis.citrate_mg,
                'cystine_mg': urine_analysis.cystine_mg,
            }

            patient_data = {
                'medical_conditions': patient_profile.medical_conditions,
                'medications': patient_profile.medications,
            }

            interpretation = interpret_24hr_urine(urine_data, patient_data)

            messages.success(request, 'Urine analysis completed successfully!')

            return render(request, 'kidney_stones_app/urine_analysis.html', {
                'urine_form': urine_form,
                'serum_form': serum_form,
                'patient_profile': patient_profile,
                'interpretation': interpretation,
                'urine_data': urine_data,
                'active_page': 'urine_analysis',
                'show_results': True
            })
    else:
        urine_form = UrineAnalysisForm()
        serum_form = SerumLabsForm()

    return render(request, 'kidney_stones_app/urine_analysis.html', {
        'urine_form': urine_form,
        'serum_form': serum_form,
        'patient_profile': patient_profile,
        'active_page': 'urine_analysis'
    })


def acute_management(request):
    """Acute Stone Management page"""
    if request.method == 'POST':
        form = AcuteManagementForm(request.POST)
        if form.is_valid():
            symptoms = {
                'uncontrolled_pain': form.cleaned_data['uncontrolled_pain'],
                'vomiting': form.cleaned_data['vomiting'],
                'fevers': form.cleaned_data['fevers'],
                'hydronephrosis': form.cleaned_data['hydronephrosis'],
                'aki': form.cleaned_data['aki'],
                'anuria': form.cleaned_data['anuria'],
            }
            stone_size = form.cleaned_data['stone_size']

            guidance = get_acute_management_guidance(symptoms, stone_size)

            return render(request, 'kidney_stones_app/acute_management.html', {
                'form': form,
                'guidance': guidance,
                'active_page': 'acute_management',
                'show_results': True
            })
    else:
        form = AcuteManagementForm()

    return render(request, 'kidney_stones_app/acute_management.html', {
        'form': form,
        'active_page': 'acute_management'
    })


def chronic_management(request):
    """Chronic Management Plan page"""
    # Get the most recent patient profile and urine analysis
    try:
        if request.user.is_authenticated:
            patient_profile = PatientProfile.objects.filter(
                user=request.user).latest('created_at')
        else:
            patient_profile = PatientProfile.objects.latest('created_at')

        urine_analysis = UrineAnalysis.objects.filter(
            patient_profile=patient_profile).latest('created_at')
        serum_labs = SerumLabs.objects.filter(
            patient_profile=patient_profile).latest('created_at')
    except (PatientProfile.DoesNotExist, UrineAnalysis.DoesNotExist):
        messages.warning(
            request, 'Please complete Patient Profile and Urine Analysis first.')
        return redirect('kidney_stones_app:patient_profile')

    if request.method == 'POST':
        form = ManagementPlanForm(request.POST)
        if form.is_valid():
            stone_type = form.cleaned_data['stone_type']

            # Convert to dict for interpretation
            urine_data = {
                'volume_L': float(urine_analysis.volume_L),
                'ph': float(urine_analysis.ph),
                'calcium_mg': urine_analysis.calcium_mg,
                'oxalate_mg': urine_analysis.oxalate_mg,
                'phosphorus_mg': urine_analysis.phosphorus_mg,
                'uric_acid_mg': urine_analysis.uric_acid_mg,
                'sodium_mEq': urine_analysis.sodium_mEq,
                'potassium_mEq': urine_analysis.potassium_mEq,
                'magnesium_mg': urine_analysis.magnesium_mg,
                'sulfate_mmol': urine_analysis.sulfate_mmol,
                'ammonium_mmol': urine_analysis.ammonium_mmol,
                'citrate_mg': urine_analysis.citrate_mg,
                'cystine_mg': urine_analysis.cystine_mg,
            }

            patient_data = {
                'medical_conditions': patient_profile.medical_conditions,
                'medications': patient_profile.medications,
            }

            serum_data = {
                'calcium_mg_dL': float(serum_labs.calcium_mg_dL),
                'intact_pth_pg_mL': serum_labs.intact_pth_pg_mL,
                'bicarbonate_mEq_L': serum_labs.bicarbonate_mEq_L,
                'potassium_mEq_L': float(serum_labs.potassium_mEq_L),
                'creatinine_mg_dL': float(serum_labs.creatinine_mg_dL),
            }

            interpretation = interpret_24hr_urine(urine_data, patient_data)
            recommendations = generate_management_plan(
                stone_type, interpretation, patient_data, serum_data)

            # Save management plan
            management_plan = ManagementPlan.objects.create(
                patient_profile=patient_profile,
                urine_analysis=urine_analysis,
                serum_labs=serum_labs,
                stone_type=stone_type,
                urine_interpretation=interpretation,
                recommendations=recommendations
            )

            return render(request, 'kidney_stones_app/chronic_management.html', {
                'form': form,
                'patient_profile': patient_profile,
                'urine_analysis': urine_analysis,
                'interpretation': interpretation,
                'recommendations': recommendations,
                'stone_type': stone_type,
                'active_page': 'chronic_management',
                'show_results': True
            })
    else:
        form = ManagementPlanForm()

    return render(request, 'kidney_stones_app/chronic_management.html', {
        'form': form,
        'patient_profile': patient_profile,
        'active_page': 'chronic_management'
    })


def educational_resources(request):
    """Educational Resources page"""
    return render(request, 'kidney_stones_app/educational_resources.html', {
        'active_page': 'educational_resources'
    })


def oxalate_finder(request):
    """Oxalate Content Finder page"""
    sort = request.GET.get('sort', 'food')
    direction = request.GET.get('direction', 'asc')
    order_prefix = '' if direction == 'asc' else '-'
    valid_sort_fields = ['food', 'type', 'oxalate_mg', 'serving_size', 'oxalate_level']
    if sort not in valid_sort_fields:
        sort = 'food'
    order_by = f'{order_prefix}{sort}'

    if request.method == 'POST':
        form = OxalateSearchForm(request.POST)
        if form.is_valid():
            search_term = form.cleaned_data['search_term']
            if search_term:
                results = OxalateContent.objects.filter(
                    Q(food__icontains=search_term) | Q(type__icontains=search_term)
                ).order_by(order_by)
            else:
                results = OxalateContent.objects.all().order_by(order_by)
        else:
            results = OxalateContent.objects.all().order_by(order_by)
    else:
        form = OxalateSearchForm()
        results = OxalateContent.objects.all().order_by(order_by)

    return render(request, 'kidney_stones_app/oxalate_finder.html', {
        'form': form,
        'results': results,
        'active_page': 'oxalate_finder',
        'request': request  # Pass request for sorting link state
    })


@csrf_exempt
def load_oxalate_data(request):
    """Load oxalate data from JSON file into database"""
    if request.method == 'POST':
        try:
            with open('oxalate_en.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            food_data_list = data.get('food_data', [])

            # Clear existing data
            OxalateContent.objects.all().delete()

            # Load new data
            for food_item in food_data_list:
                OxalateContent.objects.create(
                    food=food_item['food'],
                    type=food_item['type'],
                    oxalate_mg=food_item['oxalate_mg'],
                    serving_size=food_item['serving_size'],
                    oxalate_level=food_item['oxalate_level']
                )

            return JsonResponse({'status': 'success', 'count': len(food_data_list)})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def management_plan_detail(request, plan_id):
    """View detailed management plan"""
    management_plan = get_object_or_404(ManagementPlan, id=plan_id)

    return render(request, 'kidney_stones_app/management_plan_detail.html', {
        'management_plan': management_plan,
        'active_page': 'management_plan_detail'
    })
