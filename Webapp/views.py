from django.shortcuts import render,get_object_or_404,redirect       # Rendering, fetching objects, and redirecting
from Adminapp.models import CategoryDB           # Importing Admin models
from Adminapp.models import LocationDB           # Importing Admin models
from Webapp.models import ContactDB           # Importing Admin models
from Webapp.models import JobpostDB              # Importing Webapp models
from Webapp.models import RegistrationDB       # Importing Webapp models
from Webapp.models import UserProfile       # Importing Webapp models
from Webapp.models import JobApplicationDB     # Importing Webapp models
from django.utils.datastructures import MultiValueDictKeyError     # Handling missing file uploads
from django.core.files.storage import FileSystemStorage         # Managing file uploads
from django.contrib.auth import authenticate, login,logout      # User authentication and session management
from django.contrib.auth.models import User            # Importing Django's built-in User model
from django.utils.timezone import now, timedelta        # Working with time and session expiration
from django.contrib import messages  # Import Django messages for validation feedback
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.

# General Views

def Home(request):
    return render(request,"Home.html")
# Renders the Home page


def About_page(request):
    return render(request,"About.html")
# Renders the About Us page


def Contact_page(request):
    return render(request,"Contact.html")
# Renders the Contact Us page

def Save_contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        ContactDB.objects.create(name=name, email=email, subject=subject, message=message)
        return redirect("Contact_page")  # Redirect after saving
    return render(request, "Contact.html")




#Userprofile views

@login_required
def user_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)  # Create if not exists
    return render(request, "UserProfile.html", {"user_profile": profile})


@login_required
def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        profile.phone = request.POST.get("phone")
        profile.address = request.POST.get("address")
        if request.user.userprofile.is_employer:
            profile.company_name = request.POST.get("company_name")
        else:
            profile.job_title = request.POST.get("job_title")
        profile.save()
        return redirect("user_profile")

    return render(request, "Edit_Profile.html", {"user_profile": profile})


@login_required
def update_profile_picture(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST" and request.FILES.get("profile_picture"):
        profile.profile_picture = request.FILES["profile_picture"]
        profile.save()

    return redirect("user_profile")





# JobSeeker Views
def JobSeeker_Home(request):
    # Fetches job categories and their job counts
    categories = CategoryDB.objects.all()

    # Count jobs per category
    category_counts = {}
    for category in categories:
        job_count = JobpostDB.objects.filter(Job_Category=category.Category_Name).count()
        category_counts[category.Category_Name] = job_count

    location = LocationDB.objects.all()
    return render(request, "JobSeeker_Home.html", {
        'categories': categories,
        'location': location,
        'category_counts': category_counts
    })
# Displays the Job Seeker Home page with job categories and locations



def Job_listing(request):
    # Fetches jobs based on filters (title, location, category, job type, experience, date posted)
    job_title = request.GET.get('job_title', '')
    location = request.GET.get('location', '')
    category = request.GET.get('category', '')
    job_type = request.GET.getlist('job_type')  # Handles multiple selections
    experience = request.GET.getlist('experience')  # Handles multiple selections
    date_posted = request.GET.get('date_posted', '')
    category = request.GET.get('category', '')

    # Fetch all jobs initially
    jobs = JobpostDB.objects.all()

    # Apply filters
    if job_title:
        jobs = jobs.filter(Job_Title__icontains=job_title)
    if location:
        jobs = jobs.filter(Job_Location__icontains=location)
    if category:
        jobs = jobs.filter(Job_Category__icontains=category)
    if job_type:
        jobs = jobs.filter(Job_type__in=job_type)
    if experience:
        jobs = jobs.filter(Experience__in=experience)
    if category:
        jobs = jobs.filter(Job_Category__icontains=category)
    if date_posted:
        try:
            days = int(date_posted)
            jobs = jobs.filter(posted_at__gte=now() - timedelta(days=days))
        except ValueError:
            pass  # Ignore invalid values for date filtering

    # Fetch categories and locations for dropdowns
    categories = CategoryDB.objects.all()
    locations = LocationDB.objects.all()

    # Implement Pagination (10 jobs per page)
    paginator = Paginator(jobs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, "Job_Listing.html", {
        'page_obj': page_obj,
        'jobs': jobs,
        'categories': categories,
        'locations': locations
    })
# Displays a list of jobs with filtering options

def Job_application(request,jobs_id):
    job = JobpostDB.objects.get(id=jobs_id)
    return render(request,"Job_Application.html",context={'job':job})
# Displays the Job Application form for a specific job

def Save_application(request, jobs_id):
    # Saves job applications submitted by job seekers
    job = get_object_or_404(JobpostDB, id=jobs_id)  # Fetch job details

    if request.method == "POST":
        full_name = request.POST.get("Fullname")
        email = request.POST.get("Email")
        phone = request.POST.get("Phone")
        address = request.POST.get("Address")
        date_of_birth = request.POST.get("Dateofbirth")
        highest_qualification = request.POST.get("Highestqualification")
        university = request.POST.get("University")
        passing_year = request.POST.get("Passingyear")
        experience_years = request.POST.get("Experienceyears")
        previous_company = request.POST.get("Previouscompany")
        previous_role = request.POST.get("Previousrole")

        # Handle Resume Upload
        resume_file = None
        if 'resume' in request.FILES:
            resume = request.FILES["resume"]
            fs = FileSystemStorage()
            resume_file = fs.save(resume.name, resume)

        # Save the application in the database
        application = JobApplicationDB(
            job=job,
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            date_of_birth=date_of_birth,
            highest_qualification=highest_qualification,
            university=university,
            passing_year=passing_year,
            experience_years=experience_years,
            previous_company=previous_company,
            previous_role=previous_role,
            resume=resume_file,
            applied_on=now()
        )
        application.save()
        return redirect("Job_listing")  # Redirect to job listings or a thank-you page

    return render(request, "Job_Application.html", {"job": job})
# Saves job applications submitted by job seekers


def shortlist_candidate(request, application_id):
    application = get_object_or_404(JobApplicationDB, id=application_id)

    if application.status != "Shortlisted":  # Prevent duplicate shortlisting
        application.status = "Shortlisted"
        application.save()

        # Send Email Notification
        send_mail(
            "Congratulations! You Have Been Shortlisted",
            f"Dear {application.full_name},\n\nYou have been shortlisted for {application.job.Job_Title} at {application.job.Company_Name}. Our team will contact you soon for the next steps.\n\nBest Regards,\n{application.job.Company_Name}",
            "noreply@jobfinder.com",
            [application.email],
            fail_silently=False,
        )

        messages.success(request, f"{application.full_name} has been shortlisted!")
    else:
        messages.info(request, f"{application.full_name} is already shortlisted.")

    return redirect("Manage_jobapplication")

def Jobapplication_status(request):
    if request.user.is_authenticated:
        if request.user.is_staff:  # If the user is an employer/admin
            applications = JobApplicationDB.objects.all()  # Fetch all applications
        else:  # If the user is a job seeker
            applications = JobApplicationDB.objects.filter(email=request.user.email)

        return render(request, "Jobapplication_status.html", {"applications": applications})
    else:
        return redirect("Signin_page")  # Redirect if not logged in






# Employer Views

def Employer_Home(request):
    categories = CategoryDB.objects.all()
    location = LocationDB.objects.all()
    return render(request,"Employer_Home.html",context={'categories':categories,'location':location})
# Displays the Employer Home page

def Post_jobs(request):
    location = LocationDB.objects.all()
    categories = CategoryDB.objects.all()
    return render(request,"Post_Jobs.html",context={'location':location,'categories':categories})
# Displays the Post Job page for employers

def Save_jobpost(request):
    if request.method == "POST":
        comp_img = request.FILES["Company_Image"]
        job_tit = request.POST.get("job_title")
        job_cate = request.POST.get("job_category")
        comp_nam = request.POST.get("company_name")
        loca = request.POST.get("job_location")
        sal = request.POST.get("salary")
        job_desc = request.POST.get("job_description")
        skills = request.POST.get("required_skills")
        educ = request.POST.get("education")
        exp = request.POST.get("experience")
        job_typ = request.POST.get("job_type")
        vac = request.POST.get("vacancy")


        obj = JobpostDB(
            Company_Image=comp_img,
            Job_Title=job_tit,
            Company_Name=comp_nam,
            Job_Location=loca,
            Job_Category=job_cate,
            Job_Salary=sal,
            Job_Description=job_desc,
            Required_Skills=skills,
            Education=educ,
            Experience=exp,
            Job_type=job_typ,
            Vacancy=vac,
            posted_at=now()
        )
        obj.save()
        return redirect(Post_jobs)
# Saves job postings submitted by employers


def Manage_jobpost(request):
    job = JobpostDB.objects.all()
    categories = CategoryDB.objects.all()
    location = LocationDB.objects.all()
    return render(request,"Manage_Jobpost.html",context={'categories':categories,'location':location,'job':job})
# Displays all job posts for employers to manage

def Edit_jobpost(request,job_id):
    job = JobpostDB.objects.get(id=job_id)
    categories = CategoryDB.objects.all()
    location = LocationDB.objects.all()
    return render(request,"Edit_Jobpost.html",context={'categories':categories,'location':location,'job':job})
# fetches and displays job details for editing

def Update_jobpost(request,job_id):
    if request.method=="POST":
        update_job_cate = request.POST.get("job_category")
        update_job_tit = request.POST.get("job_title")
        update_comp_nam = request.POST.get("company_name")
        update_loca = request.POST.get("job_location")
        update_sal = request.POST.get("salary")
        update_job_desc = request.POST.get("job_description")
        update_skills = request.POST.get("required_skills")
        update_educ = request.POST.get("education")
        update_exp = request.POST.get("experience")
        update_job_typ = request.POST.get("job_type")
        update_vac = request.POST.get("vacancy")
        try:
            update_compimage = request.FILES["Company_Image"]
            fs = FileSystemStorage()
            file = fs.save(update_compimage.name, update_compimage)
        except MultiValueDictKeyError:
            file = JobpostDB.objects.get(id=job_id).Company_Image

        JobpostDB.objects.filter(id=job_id).update(Job_Title=update_job_tit,Company_Name=update_comp_nam,Job_Category=update_job_cate,
                         Job_Location=update_loca,Job_Salary=update_sal,Job_Description=update_job_desc,Required_Skills=update_skills,
                         Education=update_educ,Experience=update_exp,Job_type=update_job_typ,Vacancy=update_vac,posted_at=now(),Company_Image=file)
        return redirect(Manage_jobpost)
 # Updates job details and handles image upload

def Delete_jobpost(request,job_id):
    job=JobpostDB.objects.filter(id=job_id)
    job.delete()
    return redirect(Manage_jobpost)
# Deletes a specific job post


def Job_details(request,job_id):
    job_details = JobpostDB.objects.get(id=job_id)
    job = JobpostDB.objects.all()
    categories = CategoryDB.objects.all()
    location = LocationDB.objects.all()
    return render(request,"Job_Details.html",context={'categories':categories,'location':location,'job':job,'job_details':job_details})
# Displays detailed information about a selected job


def Manage_jobapplication(request):
    user = request.user
    if user.is_authenticated:
        if user.is_staff:  # If Employer/Admin
            applications = JobApplicationDB.objects.all()
        else:  # If Job Seeker
            applications = JobApplicationDB.objects.filter(email=user.email)

        return render(request, "Manage_Jobapplication.html", {"applications": applications})
    else:
        return redirect("Signin_page")  # Redirect to login if not logged in
# Lists all job applications for management

def View_jobapplication(request, jobs_id):
    application = get_object_or_404(JobApplicationDB, id=jobs_id)
    job_details = get_object_or_404(JobpostDB, id=application.job.id)  # Fetch job details
    return render(request, "View_Jobapplication.html", {
        "applicant": application,
        "job_details": job_details,
        "status": application.status  # Pass status to the template
    })

def Delete_jobapplication(request,job_id):
    job=JobApplicationDB.objects.filter(id=job_id)
    job.delete()
    return redirect(Manage_jobapplication)
 # Deletes a job application


def update_application_status(request, applicant_id):
    if request.method == "POST":
        application = get_object_or_404(JobApplicationDB, id=applicant_id)
        new_status = request.POST.get("status")  # Get status from the form

        if new_status in ["Shortlisted", "Rejected"]:
            application.status = new_status
            application.save()

        return redirect("View_jobapplication", jobs_id=application.id)  # Redirect back





# Authentication Views

def Signin_page(request):
    return render(request,"Signin.html")
# Renders the Signin (Login) page

def Signup_page(request):
    return render(request,"Signup.html")
# Logs out the user and redirects to the Signin page

def Signout_page(request):
    logout(request)
    return redirect("Home")
# Redirect to login page after logout

def Save_registration(request):
    if request.method == "POST":
        username = request.POST.get("username").strip()
        email = request.POST.get("email").strip()
        password = request.POST.get("pass")
        confirm_password = request.POST.get("confirmpass")

        # Validate inputs
        if len(username) < 3 or len(username) > 15 or not username.isalnum():
            messages.error(request, "Username must be between 3-15 characters and contain only letters and numbers.")
            return redirect("Signup_page")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken. Try a different one.")
            return redirect("Signup_page")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered. Try logging in.")
            return redirect("Signup_page")

        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters long.")
            return redirect("Signup_page")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("Signup_page")

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Registration successful! You can now log in.")
        return redirect("Signin_page")

    return redirect("Signup_page")
# Handles user registration and account creation


def User_login(request):
    if request.method == "POST":
        username = request.POST.get("login_username").strip()
        password = request.POST.get("login_pass")

        if username == "" or password == "":
            messages.error(request, "Username and password are required.")
            return redirect("Signin_page")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("Home")  # Redirect to job seeker home
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect("Signin_page")  # Redirect back to login
    else:
        return redirect("Signin_page")
# Handles user login authentication

