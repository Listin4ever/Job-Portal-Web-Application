from django.urls import path
from Webapp import views
from .views import update_application_status
from .views import Job_listing  # Import the view

urlpatterns=[

# General urls
    path('',views.Home, name="Home"),
    path('About_page/',views.About_page, name="About_page"),
    path('Contact_page/',views.Contact_page, name="Contact_page"),
    path('Save_contact/', views.Save_contact, name='Save_contact'),


# Userprofile urls
    path("profile/", views.user_profile, name="user_profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("profile/update_picture/", views.update_profile_picture, name="update_profile"),


# JobSeeker urls
    path('JobSeeker_Home/',views.JobSeeker_Home, name="JobSeeker_Home"),
    path('job_listing/', views.Job_listing, name='Job_listing'),
    path('Job_application/<int:jobs_id>/',views.Job_application, name="Job_application"),
    path('apply/<int:jobs_id>/',views.Save_application, name='Save_application'),
    path('update_application_status/<int:applicant_id>/', views.update_application_status, name="update_application_status"),
    path('shortlist_candidate/<int:application_id>/', views.shortlist_candidate, name="shortlist_candidate"),
    path('Jobapplication_status/', views.Jobapplication_status, name="Jobapplication_status"),

    path("profile/", views.user_profile, name="user_profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("profile/update_picture/", views.update_profile_picture, name="update_profile"),


# Employer urls
    path('Employer_Home/',views.Employer_Home, name="Employer_Home"),
    path('Post_jobs/',views.Post_jobs, name="Post_jobs"),
    path('Save_jobpost/',views.Save_jobpost, name="Save_jobpost"),
    path('Manage_jobpost/',views.Manage_jobpost, name="Manage_jobpost"),
    path('Edit_jobpost/<int:job_id>/',views.Edit_jobpost, name="Edit_jobpost"),
    path('Update_jobpost/<int:job_id>/',views.Update_jobpost, name="Update_jobpost"),
    path('Delete_jobpost/<int:job_id>/',views.Delete_jobpost, name="Delete_jobpost"),
    path('Job_details/<int:job_id>/',views.Job_details, name="Job_details"),

# Job application urls
    path('Manage_jobapplication/',views.Manage_jobapplication, name='Manage_jobapplication'),
    path('View_jobapplication/<int:jobs_id>/', views.View_jobapplication, name="View_jobapplication"),
    path('Delete_jobapplication/<int:job_id>/',views.Delete_jobapplication, name='Delete_jobapplication'),


# Authentication urls
    path('Signin_page/',views.Signin_page, name="Signin_page"),
    path('Signup_page/',views.Signup_page, name="Signup_page"),
    path('Signout_page/',views.Signout_page, name="Signout_page"),
    path('Save_registration/',views.Save_registration,name="Save_registration"),
    path('User_login/',views.User_login,name="User_login"),

]