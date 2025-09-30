from django.urls import path
from Adminapp import views

urlpatterns=[
    path('',views.Index, name = "Index"),

    #Category section
    path('Add_categories/',views.Add_categories, name = "Add_categories"),
    path('Save_categories/',views.Save_categories, name = "Save_categories"),
    path('Category_details/',views.Category_details, name = "Category_details"),
    path('Edit_categories/<int:cat_id>/',views.Edit_categories, name = "Edit_categories"),
    path('Update_categories/<int:cat_id>/',views.Update_categories, name = "Update_categories"),
    path('Delete_categories/<int:cat_id>/',views.Delete_categories, name = "Delete_categories"),


    #Location section
    path('Add_location/',views.Add_location, name = "Add_location"),
    path('Save_location/',views.Save_location, name = "Save_location"),
    path('Location_details/',views.Location_details, name = "Location_details"),
    path('Edit_location/<int:loc_id>/',views.Edit_location, name = "Edit_location"),
    path('Update_location/<int:loc_id>/',views.Update_location, name = "Update_location"),
    path('Delete_location/<int:loc_id>/',views.Delete_location, name = "Delete_location"),

    # Admin Login
    path('Admin_loginpage/',views.Admin_loginpage, name = "Admin_loginpage"),
    path('Adminlogin/',views.Adminlogin, name = "Adminlogin"),
    path('Admin_logout/',views.Admin_logout, name = "Admin_logout"),

    #Contact section
    path('Contact_details/',views.Contact_details, name = "Contact_details"),
    path('Delete_contact/<int:con_id>/',views.Delete_contact, name = "Delete_contact"),

]