from django import forms
from django.forms import ModelForm
from .models import PatientProfile, UrineAnalysis, SerumLabs


class PatientProfileForm(ModelForm):
    """Form for patient profile and medical history"""

    # Medical conditions choices
    MEDICAL_CONDITIONS = [
        ("Metabolic Syndrome", "Metabolic Syndrome"),
        ("Type 2 Diabetes", "Type 2 Diabetes"),
        ("Osteoporosis", "Osteoporosis"),
        ("Malabsorption (IBD, Bariatric Surgery, etc.)",
         "Malabsorption (IBD, Bariatric Surgery, etc.)"),
        ("Renal Tubular Acidosis", "Renal Tubular Acidosis"),
        ("Sjögren's Syndrome", "Sjögren's Syndrome"),
        ("Gout", "Gout"),
        ("Primary Hyperparathyroidism", "Primary Hyperparathyroidism"),
        ("Polycystic Kidney Disease", "Polycystic Kidney Disease"),
        ("Medullary Sponge Kidney", "Medullary Sponge Kidney"),
        ("chronic_diarrhea", "Chronic Diarrhea"),
        ("UTI with urease-producing bacteria",
         "UTI with urease-producing bacteria"),
    ]

    medical_conditions = forms.MultipleChoiceField(
        choices=MEDICAL_CONDITIONS,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text="Select all applicable conditions"
    )

    medications = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 3, 'placeholder': 'e.g., Topiramate, Hydrochlorothiazide'}),
        required=False,
        help_text="List current medications (comma-separated if multiple)"
    )

    class Meta:
        model = PatientProfile
        fields = [
            'age', 'gender', 'num_prior_stones', 'first_stone_age',
            'family_history', 'bmi', 'medical_conditions', 'medications', 'fluid_intake_L'
        ]
        widgets = {
            'age': forms.Select(choices=[(i, i) for i in range(0, 121)]),
            'gender': forms.Select(choices=PatientProfile.GENDER_CHOICES),
            'num_prior_stones': forms.Select(choices=[(i, i) for i in range(0, 21)]),
            'first_stone_age': forms.Select(choices=[(i, i) for i in range(0, 121)]),
            'bmi': forms.Select(choices=[(round(x * 0.1, 1), round(x * 0.1, 1)) for x in range(100, 501)]),
            'fluid_intake_L': forms.NumberInput(attrs={'step': 0.1, 'min': 0.5, 'max': 5.0}),
        }

    def clean_medications(self):
        """Convert comma-separated medications to list"""
        medications_text = self.cleaned_data.get('medications', '')
        if medications_text:
            return [med.strip() for med in medications_text.split(',') if med.strip()]
        return []


class UrineAnalysisForm(ModelForm):
    """Form for 24-hour urine analysis results"""

    class Meta:
        model = UrineAnalysis
        fields = [
            'volume_L', 'ph', 'calcium_mg', 'oxalate_mg', 'phosphorus_mg',
            'uric_acid_mg', 'sodium_mEq', 'potassium_mEq', 'magnesium_mg',
            'sulfate_mmol', 'ammonium_mmol', 'citrate_mg', 'cystine_mg'
        ]
        widgets = {
            'volume_L': forms.Select(choices=[(round(x * 0.1, 1), round(x * 0.1, 1)) for x in range(5, 26)]),
            'ph': forms.Select(choices=[(round(x * 0.1, 1), round(x * 0.1, 1)) for x in range(0, 15)]),
            'calcium_mg': forms.Select(choices=[(i, i) for i in range(0, 1001)]),
            'oxalate_mg': forms.Select(choices=[(i, i) for i in range(0, 101)]),
            'phosphorus_mg': forms.Select(choices=[(i, i) for i in range(0, 1001)]),
            'uric_acid_mg': forms.Select(choices=[(i, i) for i in range(0, 1001)]),
            'sodium_mEq': forms.Select(choices=[(i, i) for i in range(0, 301)]),
            'potassium_mEq': forms.Select(choices=[(i, i) for i in range(0, 301)]),
            'magnesium_mg': forms.Select(choices=[(i, i) for i in range(0, 101)]),
            'sulfate_mmol': forms.Select(choices=[(i, i) for i in range(0, 101)]),
            'ammonium_mmol': forms.Select(choices=[(i, i) for i in range(0, 101)]),
            'citrate_mg': forms.Select(choices=[(i, i) for i in range(0, 1001)]),
            'cystine_mg': forms.Select(choices=[(i, i) for i in range(0, 101)]),
        }


class SerumLabsForm(ModelForm):
    """Form for relevant serum laboratory values"""

    class Meta:
        model = SerumLabs
        fields = [
            'calcium_mg_dL', 'intact_pth_pg_mL', 'bicarbonate_mEq_L',
            'potassium_mEq_L', 'creatinine_mg_dL'
        ]
        widgets = {
            'calcium_mg_dL': forms.Select(choices=[(i, i) for i in range(0, 101)]),
            'intact_pth_pg_mL': forms.Select(choices=[(i, i) for i in range(0, 301)]),
            'bicarbonate_mEq_L': forms.Select(choices=[(i, i) for i in range(0, 101)]),
            'potassium_mEq_L': forms.Select(choices=[(i, i) for i in range(0, 101)]),
            'creatinine_mg_dL': forms.Select(choices=[(i, i) for i in range(0, 101)]),
        }


class AcuteManagementForm(forms.Form):
    """Form for acute stone management guidance"""

    # Symptoms
    uncontrolled_pain = forms.BooleanField(
        required=False, label="Uncontrolled Pain")
    vomiting = forms.BooleanField(required=False, label="Vomiting")
    fevers = forms.BooleanField(required=False, label="Fevers")
    hydronephrosis = forms.BooleanField(
        required=False, label="Hydronephrosis (on imaging)")
    aki = forms.BooleanField(required=False, label="Acute Kidney Injury")
    anuria = forms.BooleanField(required=False, label="Anuria")

    # Stone size
    STONE_SIZE_CHOICES = [
        ("< 5mm", "< 5mm"),
        ("5-10mm", "5-10mm"),
        ("> 10mm", "> 10mm"),
        ("Unknown", "Unknown"),
    ]
    stone_size = forms.ChoiceField(
        choices=STONE_SIZE_CHOICES,
        widget=forms.RadioSelect,
        initial="Unknown",
        label="Select stone size (if known)"
    )


class ManagementPlanForm(forms.Form):
    """Form for generating chronic management plan"""

    STONE_TYPE_CHOICES = [
        ("Calcium Oxalate", "Calcium Oxalate"),
        ("Calcium Phosphate", "Calcium Phosphate"),
        ("Uric Acid", "Uric Acid"),
        ("Struvite", "Struvite"),
        ("Cystine", "Cystine"),
        ("Drug-induced", "Drug-induced"),
        ("Unknown", "Unknown"),
    ]

    stone_type = forms.ChoiceField(
        choices=STONE_TYPE_CHOICES,
        initial="Calcium Oxalate",
        label="Select the primary stone type"
    )


class OxalateSearchForm(forms.Form):
    """Form for searching oxalate content"""

    search_term = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search for a food item or category...',
            'class': 'form-control'
        }),
        label="Search for a food item or category:"
    )
