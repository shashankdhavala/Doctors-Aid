from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.home,name='home'),
    path('login/', views.login_doctor, name='login'),
    path('signup/',views.signup_doctor, name='signup'),
    path('signup/verify_doctor',views.verify_doctor,name='verify'),
    path('doc_home/',views.verify_login,name='verify_login'),
    path('add_patient/',views.add_patient,name='add_patient'),
    path('view_patients/',views.view_patients,name='view_patients'),
    path('save_patients/',views.save_patient,name='save_patient'),
    path('get_records/',views.get_records,name='get_record'),
    path('patient_record/',views.patient_record,name='patient_record'),
    path('add_report/',views.add_report,name="add_report"),
     path('new_report/',views.new_report,name='new_report')



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)