from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import signup_form_doc,signup_form_patient,doctor_login,add_report_form
from .models import Doctor,Patient,Report
from .utils import pwd_strength,predict_brain_cancer,predict_malaria,predict_pneumonia
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.files import File
import PIL
'''from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload'''
# Create your views here.
# More of a request handler than a front end "view" perspective.
# View function --> Takes a request and returns a response
# Also called an action in other frameworks
# URLs need to be mapped to views


def home(request):
    return render(request, 'home.html')


def verify_login(request):
    form=doctor_login(request.POST)
    doc_username=str(request.POST['username'])
    password=str(request.POST['password'])
    #return HttpResponse("hello"+doc_username)
    #check from db

    #data=Doctor.objects.raw('select password from doctor where username=%s',[doc_username])
    data=Doctor.objects.filter(email_id=doc_username)
    if data:
        passw=data[0].password
        name=data[0].first_name
    else:
        passw=' '
    
    verified=False

    if passw==password:
        verified=True
        
    if verified:
        doc={}
        doc["id"]=data[0].doctor_id
        doc["name"]=name
        return render(request,'doc_home.html',doc)    
    else:
        messages.success(request,'Your credentials are wrong')
        return HttpResponseRedirect(reverse_lazy('login'))
    


    

def verify_doctor(request):
    #check if username is already in use
    if request.method=='POST':
        form=signup_form_doc(request.POST)
        username=str(request.POST["email_id"])
        usernames_list=Doctor.objects.values_list('email_id')
        for i in range(usernames_list.count()):
            if(username==usernames_list[i][0]):
                messages.error(request,'Email Id already taken')
                return HttpResponseRedirect(reverse_lazy('signup'))
                return HttpResponse("email taken")
        password=str(request.POST['password'])
        #if form.is_valid():
        if(pwd_strength(password)):
            form.save()
            return redirect('home')
        else:
            messages.error(request,'Your password is too weak')
            return HttpResponseRedirect(reverse_lazy('signup'))

        return redirect('signup')
        

    return HttpResponseRedirect(reverse_lazy('home'))    
    #if tests dont pass then return the details'''

def save_patient(request):
    #return HttpResponse(request)
    #fill doctor id
    doc_id=request.POST["id"]
    if request.method=='POST':
        form=signup_form_patient(request.POST)
        doc_obj=Doctor.objects.get(doctor_id=doc_id)
        model_object=Patient(first_name=request.POST["first_name"],last_name=request.POST["last_name"],Age=request.POST["Age"],Gender=request.POST["Gender"],doctor_id=doc_obj)
        doc_data=Doctor.objects.filter(doctor_id=doc_id)
        model_object.save()
        info={}
        info["id"]=doc_id
        info["name"]=doc_obj.first_name
        return render(request,'doc_home.html',info)
        #uuid gen
        #query docid
def add_patient(request):
    #return HttpResponse(request)
    context={}
    context["id"]=request.POST["id"]
    context["form"]=signup_form_patient()
    return render(request,'add_patients.html',context)

def view_patients(request):
    #return HttpResponse(request)
    doc_id=request.POST["id"]
    data=Patient.objects.filter(doctor_id_id=doc_id)
    context={}
    context["id"]=doc_id
    context["patient_data"]=data
    return render(request,'patient_list.html',context)

def get_records(request):
    #return HttpResponse(request)
    #perform query from db and replace placeholders with values for that record.html
    doc_id=request.POST["doc_id"]
    patient_id=request.POST["id"]
    #return HttpResponse("success")
    data=Report.objects.filter( patient_id_id=patient_id,doctor_id_id=doc_id )
    #add logic for no data
    patient_data=Patient.objects.filter(patient_id=patient_id)

    if data:
        context={}
        context["id"]=patient_id
        context["doc_id"]=doc_id
        context["records"]=data
        context["patient_data"]=patient_data
    else:
        context={}
        context["id"]=patient_id
        context["doc_id"]=doc_id
        context["records"]=[]
        context["patient_data"]=patient_data
        #return HttpResponse("no records to display")#change this should display empty and only add record option

    return render(request,'records_list.html',context)

def patient_record(request):
    #return HttpResponse(request)
    doc_id=request.POST["doc_id"]
    doc_obj=Doctor.objects.get(doctor_id=doc_id)
    doc_password=doc_obj.password
    doc_name=doc_obj.email_id
    id=request.POST["id"]
    report_id=request.POST["report_id"]

    data=Report.objects.filter(patient_id_id=id,doctor_id_id=doc_id,report_id=report_id)
    if data:
        pass
    else:
        return HttpResponse("fail")
    
    patient_data=Patient.objects.filter(patient_id=id)
    
    context={}
    context["report_data"]=data
    context["patient_data"]=patient_data
    context["doc_password"]=doc_password
    context["doc_name"]=doc_name

    return render(request,'display_record.html',context)

def add_report(request):
    #return HttpResponse(request)
    doc_id=request.POST["doc_id"]
    id=request.POST["id"]

    context={}
    form_obj=add_report_form()
    context["id"]=id
    context["doc_id"]=doc_id
    context["form"]=form_obj

    return render(request,'new_report.html',context)


def new_report(request):
    doc_id=request.POST["doc_id"]
    id=request.POST["id"]
    form=add_report_form(request.POST,request.FILES)
    img=request.FILES['img']
    image_name=img.name
    disease_name=request.POST["disease_name"]

    patient_data=Patient.objects.filter(patient_id=id)
    
    #write code to get report text and report url
    
    
    img_url='playground/assets/'+image_name
    if img:
        image_file = File(img)
        with open(img_url, 'wb') as f:
            f.write(image_file.read())

    db_img_url="http://127.0.0.1:8000/media/"+image_name
    predict_image_url='playground/assets/'+image_name
    if disease_name=="Malaria":
        report_image,report_label,report_probability=predict_malaria(predict_image_url,100)
    elif disease_name=="Brain Cancer":
        report_image,report_label,report_probability=predict_brain_cancer(predict_image_url,240)
    elif disease_name=="Pneumonia":
        report_image,report_label,report_probability=predict_pneumonia(predict_image_url,240)

    db_report_url="http://127.0.0.1:8000/media/"+id+disease_name+'.png'
    
    #if report_image:
    '''image_file = File(report_image)
    with open(report_url, 'wb') as f:
        f.write(image_file.read())'''
    save_report_url='playground/assets/'+id+disease_name+'.png'
    report_image.save(save_report_url,format='PNG')

    report_probabilty=report_probability.tostring()

    report_text=str(report_label)+" with a probability:"+str(report_probability)
    #get report image save it in asses put url in db 
    #getreport text also 
    model_obj=Report(Report_text=report_text,Report_URL=db_report_url,disease_name=disease_name,patient_id_id=id,doctor_id_id=doc_id,Image_URL=db_img_url)
    model_obj.save()

    

    #save in db also
    
    #http://127.0.0.1:8000/media/DSC_1249.jpg-1.JPG
    context={}
    context["id"]=id
    context["doc_id"]=doc_id
    data=Report.objects.filter(patient_id_id=id,doctor_id_id=doc_id )
    context["records"]=data
    context["patient_data"]=patient_data
    
    return render(request,'records_list.html',context)

    
    #write logic to upload in drive and retrieve url ,then save url in db

def login_doctor(request):
    context={}
    context["form"]=doctor_login()
    return render(request,'login.html',context)

def signup_doctor(request):
    context={}
    context["form"]=signup_form_doc()
    return render(request,'doctor_signup.html',context)

def signup_patient(request):
    context={}
    context["form"]=signup_form_patient()
    return render(request,'',context)

