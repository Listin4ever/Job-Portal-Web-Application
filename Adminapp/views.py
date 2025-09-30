from django.shortcuts import render,redirect
from Adminapp.models import CategoryDB
from Adminapp.models import LocationDB
from Webapp.models import ContactDB
from django.utils.datastructures import MultiValueDictKeyError
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login

# Create your views here.

#Root page
def Index(request):
    return render(request,"Index.html")


#Category section
def Add_categories(request):
    return render(request,"Add_Categories.html")

def Save_categories(request):
    if request.method == "POST":
        Cate = request.POST.get("Categories_name")
        cate_img = request.FILES["Category_Image"]

        obj = CategoryDB(Category_Name=Cate,Category_Image=cate_img)
        obj.save()
        return redirect(Add_categories)

def Category_details(request):
    categories = CategoryDB.objects.all()
    return render(request,"Display_Categories.html", context={'categories':categories})

def Edit_categories(request,cat_id):
    categories = CategoryDB.objects.get(id=cat_id)
    return render(request,"Edit_Categories.html",context={'categories':categories})

def Update_categories(request,cat_id):
    if request.method=="POST":
        update_name = request.POST.get("Categories_name")
        try:
            update_image = request.FILES["Category_Image"]
            fs = FileSystemStorage()
            file = fs.save(update_image.name, update_image)
        except MultiValueDictKeyError:
            file = CategoryDB.objects.get(id=cat_id).Category_Image

        CategoryDB.objects.filter(id=cat_id).update(Category_Name=update_name,
                                                         Category_Image=file)
        return redirect(Category_details)



def Delete_categories(request,cat_id):
    Categories=CategoryDB.objects.filter(id=cat_id)
    Categories.delete()
    return redirect(Category_details)


#-----------------------------------------------------------------------------------------------------------------------



#Location section
def Add_location(request):
    return render(request,"Add_Location.html")

def Save_location(request):
    if request.method == "POST":
        Loc = request.POST.get("L_Location")
        obj = LocationDB(Location=Loc)
        obj.save()
        return redirect(Add_location)

def Location_details(request):
    location = LocationDB.objects.all()
    return render(request,"Display_Location.html", context={'location':location})

def Edit_location(request,loc_id):
    location = LocationDB.objects.get(id=loc_id)
    return render(request,"Edit_Location.html",context={'location':location})

def Update_location(request,loc_id):
    if request.method=="POST":
        update_location = request.POST.get("L_Location")

        LocationDB.objects.filter(id=loc_id).update(Location=update_location)
        return redirect(Location_details)

def Delete_location(request,loc_id):
    location=LocationDB.objects.filter(id=loc_id)
    location.delete()
    return redirect(Location_details)

#-------------------------------------------------------------------------------------------------------------------------



#Login & Logout Section
def Admin_loginpage(request):
    return render(request,"Admin_Login.html")

def Adminlogin(request):
    if request.method == "POST":
        un = request.POST.get("admin_username")
        pswd = request.POST.get("admin_password")

        user = authenticate(username=un, password=pswd)
        if user is not None:
            login(request, user)
            request.session["username"] = un  # Store username in session
            return redirect(Index)
        else:
            return redirect(Admin_loginpage)
    return redirect(Admin_loginpage)

def Admin_logout(request):
    request.session.flush()  # Clears all session data
    return redirect(Admin_loginpage)


#------------------------------------------------------------------------------------------------------------------------------

# Contact Deatils view

def Contact_details(request):
    contact = ContactDB.objects.all()
    return render(request,"Contact_details.html", context={'contact':contact})

def Delete_contact(request,con_id):
    contact = ContactDB.objects.filter(id=con_id)
    contact.delete()
    return redirect(Contact_details)