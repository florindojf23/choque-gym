from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from custom.models import *
from custom.utils import *
from cliente.models import *
from .forms import *
import os
import csv
import datetime
import chardet
import logging
from django.db import IntegrityError
from .forms import UploadCSVForm
from .models import Member, Tinan, Municipality
from django.conf import settings

#pdf lib
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa

# Create your views here.
@login_required
def member(request):
    listamembru = Member.objects.all()
    data = {
    'title':"Lista Membru",
    'active_estudante':"active",
    'dadus':listamembru
    }
    return render(request, 'listamember.html',data)

@login_required
def createMember(request):
    tinan = Tinan.objects.all().order_by('-id')
    form = MemberForm()

    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('member')
    data = {
        'form':form,
        'listaTinan':tinan,
        'title':"Formulariu Membru",
        'page':"form",
    }
    return render(request, 'formmember.html',data)

@login_required
def updateMember(request, id):
    tinan = Tinan.objects.all().order_by('-id')
    member= Member.objects.get(id=id)
    form = MemberForm(instance=member)

    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            return redirect('member')
    data = {
        'form':form,
        'tinan':tinan,
        'title':"Formulariu Update Membru",
        'page':"form",
    }
    return render(request, 'formmember.html',data)

@login_required
def deleteMember(request,pk):
    member = Member.objects.get(id=pk)
    member.delete()
    return redirect('member')

@login_required
def detailMember(request,pk):
    memberData = get_object_or_404(Member,id=pk)
    data = {
    'title':"Detallu member",
    'memberData':memberData,
    'page':"view",
    'active_estudante':"active",
    }
    return render(request, 'formmember.html',data)

@login_required
def csv_member(request):
    # replace with the fields you need 
    fields = ['nu_id','naran','sexo','naturalidade','join_date','end_date','enderesu','municipio__name','status__name','phone','email']
    # Generate the csv file with datetime
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f"attachment; filename=listamemberGeral.csv"
    writer = csv.writer(response)
    # Write the header row
    writer.writerow(fields)
    # Use the fields to get the data, specifying the model name
    for row in Member.objects.values(*fields):
        writer.writerow([row[field] for field in fields])
        # return
    return response

@login_required
def pdf_member(request):
    member = Member.objects.all()
    data = {'dadus':member,
            'title':"PDF Docs"}
    pdf = render_to_pdf('pdf/memberpdf.html',data)
    return HttpResponse(pdf,content_type='application/pdf')

def render_to_pdf(template_src,context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type='application/pdf')
    return None

@login_required
def upload_csv(request):
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csvfile = request.FILES['csv_file']
            
            # Detect file encoding
            raw_data = csvfile.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            
            # Decode file content
            decoded_file = raw_data.decode(encoding).splitlines()
            reader = csv.reader(decoded_file, delimiter=';')

            # Skip the header row
            next(reader)

            errors = []

            for row in reader:
                # Ensure the row has enough columns
                if len(row) < 14:
                    errors.append(f"Skipping row (not enough columns): {row}")
                    continue

                try:
                    # Check if a Funcionariu with the same `nu` already exists
                    if Member.objects.filter(nu_id=row[0]).exists():
                        errors.append(f"Skipping duplicate row with nu_id: {row[0]}")
                        continue

                    # Create a new Funcionariu object
                    new_member = Member.objects.create(
                        nu_id=row[0],
                        nome_completo=row[1],
                        sexo=row[2],
                        naturalidade=row[3],
                        data_do_nasc=row[4],
                        data_entrada=row[5],
                        validade=row[6],
                        posição=row[7],
                        direção=row[8],
                        endereço=row[9],
                        município_id=row[10],
                        estatuto_id=row[11],
                        nu_contacto=row[12],
                        email=row[13]
                        # Uncomment and handle these fields if necessary
                        # fotografia=row[14] if row[14] else None,
                        # documentos=row[15] if row[15] else None
                    )
                    print(f"Created Funcionariu: {new_member}")
                except IntegrityError as e:
                    print(f"IntegrityError: {e}")
                except Exception as e:
                    print(f"Error creating Funcionariu: {e}")
            
            return render(request, 'success.html')
        else:
            print(f"Form is not valid: {form.errors}")
    else:
        form = UploadCSVForm()
    return render(request, 'upload_csv.html', {'form': form})

def upload_success(request):
    return render(request, 'success.html')


#Gym Class Views
@login_required
def gymclass(request):
    listagymclass = GymClass.objects.all()
    data = {
    'title':"Lista Gym Class",
    'active_estudante':"active",
    'dadus':listagymclass
    }
    return render(request, 'listagymclass.html',data)

@login_required
def createGymClass(request):
    form = GymClassForm()

    if request.method == 'POST':
        form = GymClassForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gymclass')
    data = {
        'form':form,
        'title':"Formulariu Gym Class",
        'page':"form",
    }
    return render(request, 'gymclassform.html',data)

@login_required
def updateGymClass(request, id):
    gymclass= GymClass.objects.get(id=id)
    form = GymClassForm(instance=gymclass)

    if request.method == 'POST':
        form = GymClassForm(request.POST, request.FILES, instance=gymclass)
        if form.is_valid():
            form.save()
            return redirect('gymclass')
    data = {
        'form':form,
        'title':"Formulariu Update Gym Class",
        'page':"form",
    }
    return render(request, 'gymclassform.html',data)

@login_required
def deleteGymClass(request,pk):
    gymclass = GymClass.objects.get(id=pk)
    gymclass.delete()
    return redirect('gymclass')

@login_required
def detailGymClass(request,pk):
    gymclassdata = get_object_or_404(GymClass,id=pk)
    data = {
    'title':"Detallu Gym Class",
    'gymclassdata':gymclassdata,
    'page':"view",
    'active_estudante':"active",
    }
    return render(request, 'gymclassform.html',data)

@login_required
def csv_gymclass(request):
    # replace with the fields you need 
    fields = ['name','description','start_time','end_time','days_of_week','payment_per_month']
    # Generate the csv file with datetime
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f"attachment; filename=listagymclass.csv"
    writer = csv.writer(response)
    # Write the header row
    writer.writerow(fields)
    # Use the fields to get the data, specifying the model name
    for row in GymClass.objects.values(*fields):
        writer.writerow([row[field] for field in fields])
        # return
    return response

@login_required
def pdf_gymclass(request):
    gymclass = GymClass.objects.all()
    data = {'dadus':gymclass,
            'title':"PDF Docs"}
    pdf = render_to_pdf('pdf/gymclasspdf.html',data)
    return HttpResponse(pdf,content_type='application/pdf')

def render_to_pdf(template_src,context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type='application/pdf')
    return None

#Enrollments
@login_required
def enrollment(request):
    listaenrollment = Enrollment.objects.all()
    data = {
    'title':"Lista Enrollments",
    'active_estudante':"active",
    'dadus':listaenrollment
    }
    return render(request, 'listaenroll.html',data)

@login_required
def createEnrollment(request):
    form = EnrollmentForm()

    if request.method == 'POST':
        form = EnrollmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('enrollment')
    data = {
        'form':form,
        'title':"Formulariu Enrollments",
        'page':"form",
    }
    return render(request, 'enrollform.html',data)

@login_required
def updateEnrollment(request, id):
    enrollment= Enrollment.objects.get(id=id)
    form = EnrollmentForm(instance=enrollment)

    if request.method == 'POST':
        form = EnrollmentForm(request.POST, request.FILES, instance=enrollment)
        if form.is_valid():
            form.save()
            return redirect('enrollment')
    data = {
        'form':form,
        'title':"Formulariu Update Enrollment",
        'page':"form",
    }
    return render(request, 'enrollform.html',data)

@login_required
def deleteEnrollment(request,pk):
    enrollform = Enrollment.objects.get(id=pk)
    enrollform.delete()
    return redirect('enrollment')

@login_required
def detailEnrollment(request,pk):
    enrolldata = get_object_or_404(Enrollment,id=pk)
    data = {
    'title':"Detallu Enrolment",
    'enrolldata':enrolldata,
    'page':"view",
    'active_estudante':"active",
    }
    return render(request, 'enrollform.html',data)

@login_required
def csv_enroll(request):
    # Define the fields you want to include in the CSV
    fields = ['member__naran', 'gym_class__name', 'enrollment_date', 'get_total_payment']

    # Generate the CSV file with datetime
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="listaenroll.csv"'
    writer = csv.writer(response)

    # Write the header row
    writer.writerow(['Member Name', 'Gym Class Name', 'Enrollment Date', 'Total Payment'])  # Custom header row

    # Retrieve data from the Enrollment model and write rows to CSV
    enrollments = Enrollment.objects.all()
    for enrollment in enrollments:
        total_payment = enrollment.get_total_payment()  # Calculate total payment using the method
        row = [
            enrollment.member.naran,
            enrollment.gym_class.name,
            enrollment.enrollment_date,
            total_payment if total_payment is not None else ''  # Handle None values gracefully
        ]
        writer.writerow(row)

    return response

@login_required
def pdf_enroll(request):
    enrollment = Enrollment.objects.all()
    data = {'dadus':enrollment,
            'title':"PDF Docs"}
    pdf = render_to_pdf('pdf/enrollpdf.html',data)
    return HttpResponse(pdf,content_type='application/pdf')

def render_to_pdf(template_src,context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type='application/pdf')
    return None

