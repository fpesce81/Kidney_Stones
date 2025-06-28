from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class PatientProfile(models.Model):
    """Model to store patient profile and medical history"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Basic Information
    age = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(120)],
        help_text="Patient age in years"
    )
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    num_prior_stones = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        help_text="Number of prior stone episodes"
    )
    first_stone_age = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(120)],
        null=True, blank=True,
        help_text="Age of first stone episode"
    )
    family_history = models.BooleanField(default=False)
    bmi = models.DecimalField(
        max_digits=4, decimal_places=1,
        validators=[MinValueValidator(10.0), MaxValueValidator(50.0)],
        help_text="BMI in kg/m²"
    )

    # Medical Conditions (stored as JSON field for flexibility)
    medical_conditions = models.JSONField(default=list, blank=True)
    medications = models.JSONField(default=list, blank=True)

    # Dietary Information
    fluid_intake_L = models.DecimalField(
        max_digits=3, decimal_places=1,
        validators=[MinValueValidator(0.5), MaxValueValidator(5.0)],
        help_text="Daily fluid intake in liters"
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Patient {self.id} - {self.age}yo {self.gender}"


class UrineAnalysis(models.Model):
    """Model to store 24-hour urine analysis results"""
    patient_profile = models.ForeignKey(
        PatientProfile, on_delete=models.CASCADE, related_name='urine_analyses')
    created_at = models.DateTimeField(auto_now_add=True)

    # Volume and pH
    volume_L = models.DecimalField(
        max_digits=3, decimal_places=1,
        validators=[MinValueValidator(0.5), MaxValueValidator(2.5)],
        help_text="24-hour urine volume in liters"
    )
    ph = models.DecimalField(
        max_digits=3, decimal_places=1,
        validators=[MinValueValidator(0.0), MaxValueValidator(14.0)],
        help_text="Urine pH"
    )

    # Minerals
    calcium_mg = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(1000)],
        help_text="Calcium in mg/d"
    )
    oxalate_mg = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Oxalate in mg/d"
    )
    phosphorus_mg = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(1000)],
        help_text="Phosphorus in mg/d"
    )
    uric_acid_mg = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(1000)],
        help_text="Uric acid in mg/d"
    )

    # Electrolytes
    sodium_mEq = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(300)],
        help_text="Sodium in mEq/d"
    )
    potassium_mEq = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(300)],
        help_text="Potassium in mEq/d"
    )
    magnesium_mg = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Magnesium in mg/d"
    )

    # Other parameters
    sulfate_mmol = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Sulfate in mmol/d"
    )
    ammonium_mmol = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Ammonium in mmol/d"
    )
    citrate_mg = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(1000)],
        help_text="Citrate in mg/d"
    )
    cystine_mg = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0,
        help_text="Cystine in mg/d (optional)"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Urine analyses"

    def __str__(self):
        return f"Urine Analysis {self.id} - {self.patient_profile}"


class SerumLabs(models.Model):
    """Model to store relevant serum laboratory values"""
    patient_profile = models.ForeignKey(
        PatientProfile, on_delete=models.CASCADE, related_name='serum_labs')
    created_at = models.DateTimeField(auto_now_add=True)

    calcium_mg_dL = models.DecimalField(
        max_digits=4, decimal_places=1,
        validators=[MinValueValidator(0.0), MaxValueValidator(20.0)],
        help_text="Serum calcium in mg/dL"
    )
    intact_pth_pg_mL = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(300)],
        help_text="Intact PTH in pg/mL"
    )
    bicarbonate_mEq_L = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Bicarbonate in mEq/L"
    )
    potassium_mEq_L = models.DecimalField(
        max_digits=3, decimal_places=1,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        help_text="Serum potassium in mEq/L"
    )
    creatinine_mg_dL = models.DecimalField(
        max_digits=4, decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(20.0)],
        help_text="Serum creatinine in mg/dL"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Serum labs"

    def __str__(self):
        return f"Serum Labs {self.id} - {self.patient_profile}"


class OxalateContent(models.Model):
    """Model to store oxalate content of foods"""
    food = models.CharField(max_length=200, help_text="Food item name")
    type = models.CharField(max_length=100, help_text="Food category/type")
    oxalate_mg = models.DecimalField(
        max_digits=6, decimal_places=2,
        help_text="Oxalate content in mg per serving"
    )
    serving_size = models.CharField(
        max_length=100, help_text="Serving size description")
    oxalate_level = models.CharField(
        max_length=20,
        choices=[
            ('Low', 'Low'),
            ('Medium', 'Medium'),
            ('High', 'High'),
            ('Very High', 'Very High'),
        ],
        help_text="Oxalate level classification"
    )

    class Meta:
        ordering = ['food']

    def __str__(self):
        return f"{self.food} ({self.oxalate_level})"


class ManagementPlan(models.Model):
    """Model to store generated management plans"""
    patient_profile = models.ForeignKey(
        PatientProfile, on_delete=models.CASCADE, related_name='management_plans')
    urine_analysis = models.ForeignKey(
        UrineAnalysis, on_delete=models.CASCADE, related_name='management_plans')
    serum_labs = models.ForeignKey(
        SerumLabs, on_delete=models.CASCADE, related_name='management_plans', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    STONE_TYPE_CHOICES = [
        ('Calcium Oxalate', 'Calcium Oxalate'),
        ('Calcium Phosphate', 'Calcium Phosphate'),
        ('Uric Acid', 'Uric Acid'),
        ('Struvite', 'Struvite'),
        ('Cystine', 'Cystine'),
        ('Drug-induced', 'Drug-induced'),
        ('Unknown', 'Unknown'),
    ]
    stone_type = models.CharField(max_length=20, choices=STONE_TYPE_CHOICES)

    # Store interpretation and recommendations as JSON
    urine_interpretation = models.JSONField(
        default=dict, help_text="Urine analysis interpretation")
    recommendations = models.JSONField(
        default=list, help_text="Management recommendations")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Management Plan {self.id} - {self.stone_type} for {self.patient_profile}"
