from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/<slug:slug>/', views.course_detail, name='course_detail'),
    path('about/', views.about, name='about'),
]