from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password_step1, name='forgot_password_step1'),
    path('forgot-password/verify/', views.forgot_password_step2, name='forgot_password_step2'),
    path('forgot-password/reset/', views.forgot_password_reset, name='forgot_password_reset'),
    path('qa/', views.qa_list, name='qa_list'),
    path('search/', views.search, name='search'),
    path('course/<slug:subject_slug>/', views.subject_detail, name='subject_detail'),
    path('course/<slug:subject_slug>/<slug:chapter_slug>/', views.subject_detail, name='chapter_detail'),
]
