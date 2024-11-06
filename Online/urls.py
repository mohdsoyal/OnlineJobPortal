"""
URL configuration for JobPortal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path 
from django.conf import settings
from django.conf.urls.static import static
from . import views
 

urlpatterns = [
    
    path('',views.index , name='index'),
    path('latest_job',views.letest_job,name='letest_job'),
    path('contact',views.contact_us,name='contact'),
    path('search',views.search,name='search'),
    path('job-posting-chart/', views.job_posting_chart, name='job_posting_chart'),
     path('application-percentage-chart/',views.job_application_percentage_chart, name='job_application_percentage_chart'),
    path('adminPage',views.admin,name='adminPage'),
    path('admin_home',views.admin_home,name='admin_home'),
    path('changepassword',views.ChangeAdminPassword,name='changepassword'),
    
    
    # Recuiter urls................................................
    path('recuiternavbar',views.RecuiterNavbar,name='recuiternavbar'),
    path('recuruiter',views.RecruiterLogin,name='recruiter'),
    path('recruiterSignup',views.RecruiterSignup,name='recruiterSignup'),
    path('recuiter_home',views.recuiter_home,name='recruiter_home'),
    path('RecuiterPendding',views.RecuiterPennding,name='RecuiterPendding'),
    path('changestatus/<id>',views.ChangeStatus,name='change_status'),
    path('recuiteraccepted',views.RecuiterAccepted,name='accepted'),
    path('recuiterrejected',views.RecuiterRejected,name='rejected'),
    path('allrecuiter',views.AllRecuiter,name='allrecuiter'),
    path('recuiterpass',views.RecuiterChangePassword,name='recuiterpass'),
    path('jobadd',views.add_job,name='add_job'),
    path('job_list',views.jobList,name='job_list'),
    path('jonDelete/<id>',views.JobDelete,name='jobdelete'),
    path('jobUpdate/<id>',views.JobUpdate,name='jobUpdate'),
    path('recuiterProfile',views.Recruiter_profile,name='recuiterProfile'),
    path('edit_profile/', views.edit_recruiter_profile, name='edit_recruiter_profile'),

    
    # User url.....................................................
    path('user_login',views.UserLogin,name='user_login'),
    path('user_signup',views.Usersignup,name='Signup'),
    path('user_home',views.user_home,name='home'),
    path('view_user',views.view_user,name='view_user'),
    path('UserDelete/<id>',views.UserDelete,name='userDelete'),
    path('changeuserpassword',views.ChangeUserPassword,name='changeuserpassword'),
    path('userLogout',views.userLogout,name='userLogout'),
    path('UserProfile',views.User_profile,name='userprofile'),
    path('profile_edit/',views.edit_user_profile,name='userprofileedit'),
    path('userjoblist',views.user_latest_job,name='userJobList'),
    path('job_details/<id>',views.job_details,name='job_detalis'),
    path('applyjob/<id>',views.apply_for_job,name='applyjob'),
    path('condidateapply',views.Condidate_apply,name='condidateapply'),
    
    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
