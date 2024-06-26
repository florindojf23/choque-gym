from django.urls import path
from .views import *

urlpatterns=[
	path('member',member, name='member'),
	path('create_member', createMember, name='create_member'),
	path('update_member/<str:id>', updateMember, name='update_member'),
	path('delete_member/<str:pk>', deleteMember, name='delete_member'),
	path('detail_member/<str:pk>', detailMember,  name = 'detail_member'),
	path('csv_member/', csv_member, name="csv_member"),
	path('pdf_member/', pdf_member, name="pdf_member"),
	path('upload_csv/', upload_csv, name='upload_csv'),
    path('upload_success/', upload_success, name='upload_success'),

    path('gymclass',gymclass, name='gymclass'),
	path('create_gym_class', createGymClass, name='create_gym_class'),
	path('update_gym_class/<str:id>', updateGymClass, name='update_gym_class'),
	path('delete_gym_class/<str:pk>', deleteGymClass, name='delete_gym_class'),
	path('detail_gymclass/<str:pk>', detailGymClass,  name = 'detail_gymclass'),
	path('csv_gymclass/', csv_gymclass, name="csv_gymclass"),
	path('pdf_gymclass/', pdf_gymclass, name="pdf_gymclass"),

	path('enrollment',enrollment, name='enrollment'),
	path('create_enrollment', createEnrollment, name='create_enrollment'),
	path('update_enrollment/<str:id>', updateEnrollment, name='update_enrollment'),
	path('delete_enrollment/<str:pk>', deleteEnrollment, name='delete_enrollment'),
	path('detail_enrollment/<str:pk>', detailEnrollment,  name = 'detail_enrollment'),
	path('csv_enroll/', csv_enroll, name="csv_enroll"),
	path('pdf_enroll/', pdf_enroll, name="pdf_enroll"),


	
]
