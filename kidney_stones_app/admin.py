from django.contrib import admin
from .models import PatientProfile, UrineAnalysis, SerumLabs, OxalateContent, ManagementPlan


@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'age', 'gender',
                    'num_prior_stones', 'bmi', 'created_at']
    list_filter = ['gender', 'family_history', 'created_at']
    search_fields = ['id', 'age', 'gender']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('age', 'gender', 'num_prior_stones', 'first_stone_age', 'family_history', 'bmi')
        }),
        ('Medical Information', {
            'fields': ('medical_conditions', 'medications')
        }),
        ('Dietary Information', {
            'fields': ('fluid_intake_L',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UrineAnalysis)
class UrineAnalysisAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient_profile', 'volume_L',
                    'ph', 'calcium_mg', 'oxalate_mg', 'created_at']
    list_filter = ['created_at', 'ph']
    search_fields = ['patient_profile__id']
    readonly_fields = ['created_at']

    fieldsets = (
        ('Patient Information', {
            'fields': ('patient_profile',)
        }),
        ('Volume and pH', {
            'fields': ('volume_L', 'ph')
        }),
        ('Minerals', {
            'fields': ('calcium_mg', 'oxalate_mg', 'phosphorus_mg', 'uric_acid_mg')
        }),
        ('Electrolytes', {
            'fields': ('sodium_mEq', 'potassium_mEq', 'magnesium_mg')
        }),
        ('Other Parameters', {
            'fields': ('sulfate_mmol', 'ammonium_mmol', 'citrate_mg', 'cystine_mg')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(SerumLabs)
class SerumLabsAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient_profile', 'calcium_mg_dL',
                    'intact_pth_pg_mL', 'bicarbonate_mEq_L', 'created_at']
    list_filter = ['created_at']
    search_fields = ['patient_profile__id']
    readonly_fields = ['created_at']

    fieldsets = (
        ('Patient Information', {
            'fields': ('patient_profile',)
        }),
        ('Laboratory Values', {
            'fields': ('calcium_mg_dL', 'intact_pth_pg_mL', 'bicarbonate_mEq_L', 'potassium_mEq_L', 'creatinine_mg_dL')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(OxalateContent)
class OxalateContentAdmin(admin.ModelAdmin):
    list_display = ['food', 'type', 'oxalate_mg',
                    'serving_size', 'oxalate_level']
    list_filter = ['oxalate_level', 'type']
    search_fields = ['food', 'type']
    ordering = ['food']

    fieldsets = (
        ('Food Information', {
            'fields': ('food', 'type')
        }),
        ('Oxalate Content', {
            'fields': ('oxalate_mg', 'serving_size', 'oxalate_level')
        }),
    )


@admin.register(ManagementPlan)
class ManagementPlanAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient_profile', 'stone_type', 'created_at']
    list_filter = ['stone_type', 'created_at']
    search_fields = ['patient_profile__id', 'stone_type']
    readonly_fields = ['created_at']

    fieldsets = (
        ('Patient Information', {
            'fields': ('patient_profile', 'urine_analysis', 'serum_labs')
        }),
        ('Plan Details', {
            'fields': ('stone_type', 'urine_interpretation', 'recommendations')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
