from django.shortcuts import render
from .models import *
from cliente.models import Member,GymClass,Enrollment
from custom.models import *
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from datetime import date, timedelta
from django.db.models import Count
from django.http import JsonResponse


# Create your views here.
@login_required
def dashboard(request):
    context = {
        "title":"Dashboard",
        "active_varanda":"active",
    }
    return render(request,'main/dashboard.html',context)

@login_required
def dashboard(request):
    total_member = Member.objects.count()
    mane = Member.objects.filter(sexo='Mane').count()
    feto = Member.objects.filter(sexo='Feto').count()
    context = {
        'total_member': total_member,
        'mane': mane,
        'feto': feto,
    }
    return render(request, 'main/dashboard.html', context)

class MyPasswordChangeView(PasswordChangeView):
    template_name = 'main/change_password.html'
    success_url = reverse_lazy('password_change_done')

class MyPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'main/password_change_done.html'

@login_required
def todays_schedule(request):
    today = date.today().strftime("%A")  # Get current day of the week as string
    classes_today = GymClass.objects.filter(days_of_week__icontains=today)
    
    context = {
        'today': today,
        'classes_today': classes_today,
    }
    return render(request, 'main/todays_schedule.html', context)

@login_required
def weekly_schedule(request):
    today = date.today()
    week_days = [(today + timedelta(days=i)).strftime("%A") for i in range(7)]  # List of days in the week starting from today
    weekly_classes = {day: GymClass.objects.filter(days_of_week__icontains=day) for day in week_days}
    
    context = {
        'week_days': week_days,
        'weekly_classes': weekly_classes,
    }
    return render(request, 'main/weekly_schedule.html', context)

@login_required
def member_report(request):
    members = Member.objects.all()
    return render(request, 'main/member_report.html', {'members': members})

@login_required
def class_report(request):
    classes = GymClass.objects.all()
    return render(request, 'main/class_report.html', {'classes': classes})

@login_required
def enrollment_report(request):
    enrollments = Enrollment.objects.select_related('member', 'gym_class').all()
    return render(request, 'main/enrollment_report.html', {'enrollments': enrollments})

@login_required
def charts(request):
	data = {
	'title':"Charts"
	}
	return render(request,'main/charts.html',data)

def chart_seksu_member(request):
	labels = []
	data = []
	queryset = Member.objects.values('sexo').annotate(total_seksu=Count('sexo'))
	for item in queryset:
		labels.append(item['sexo'])
		data.append(item['total_seksu'])
	return JsonResponse(data={
		'labels':labels,
		'data':data,
		})

def chart_municipiu(request):
	labels = []
	data = []
	queryset = Member.objects.values('municipio__name').annotate(total_municipiu=Count('municipio__name'))
	for item in queryset:
		labels.append(item['municipio__name'])
		data.append(item['total_municipiu'])
	return JsonResponse(data={
		'labels':labels,
		'data':data,
		})


