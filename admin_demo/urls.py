from django.urls import path
from . import views

urlpatterns = [
path('',views.adminlogin,name='admin-login'),
path('admin-home/',views.adminhome,name='admin-home'),
path('admin-logout/',views.adminlogout,name='admin-logout'),
path('admin-delete/<str:id>/', views.admindelete,name='admin-delete'),
path('admin-update/<int:id>/',views.adminupdate,name='admin-update'),
path('admin-register/',views.adminregister,name='admin-register')
]