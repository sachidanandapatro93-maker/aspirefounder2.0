from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/<slug:slug>/', views.course_detail, name='course_detail'),
    path('about/', views.about, name='about'),
    
    # Place success ABOVE the slug pattern!
    path('enroll/success/', views.enrollment_success, name='enrollment_success'),
    
    path('enroll/<slug:slug>/', views.checkout_view, name='checkout'),
]