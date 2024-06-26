from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
from .views import dashboard
from . import views
from .views import MyPasswordChangeView, MyPasswordChangeDoneView

urlpatterns = [
	path('', dashboard, name="home"),
	path('dashboard',dashboard, name='dashboard'),
	path('change-password/', MyPasswordChangeView.as_view(), name='change_password'),
    path('password-change-done/', MyPasswordChangeDoneView.as_view(), name='password_change_done'),
	path('schedule/today/', views.todays_schedule, name='todays_schedule'),
    path('schedule/week/', views.weekly_schedule, name='weekly_schedule'),
	path('reports/members/', views.member_report, name='member_report'),
    path('reports/classes/', views.class_report, name='class_report'),
    path('reports/enrollments/', views.enrollment_report, name='enrollment_report'),
	path('charts/', charts, name="charts"),
	path('chart_seksu_member/', chart_seksu_member, name="chart_seksu_member"),
	path('chart_municipiu/', chart_municipiu, name="chart_municipiu"),

]