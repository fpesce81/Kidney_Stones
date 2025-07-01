from django.urls import path
from . import views

app_name = 'kidney_stones_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('patient-profile/', views.patient_profile, name='patient_profile'),
    path('urine-analysis/', views.urine_analysis, name='urine_analysis'),
    path('acute-management/', views.acute_management, name='acute_management'),
    path('chronic-management/', views.chronic_management,
         name='chronic_management'),
    path('educational-resources/', views.educational_resources,
         name='educational_resources'),
    path('oxalate-finder/', views.oxalate_finder, name='oxalate_finder'),
    path('management-plan/<int:plan_id>/',
         views.management_plan_detail, name='management_plan_detail'),
    path('load-oxalate-data/', views.load_oxalate_data, name='load_oxalate_data'),
]
