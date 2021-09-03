from django.urls import path
from . import views

urlpatterns = [
	path('hello/', views.say),
	path('l/', views.livefe),
	path('s/', views.stream, name='livefe'),
	path('st/', views.stream1),
	path('st/d/', views.delete_record1),
	path('apiv/', views.FileUploadView1.as_view(), name="apiv"),
	]
