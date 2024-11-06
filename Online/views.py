from django.shortcuts import render ,redirect
from .models import StudentUser,Recruiter ,Jobs ,Apply
from django.contrib.auth.models import User
from  django.contrib.auth import authenticate , login ,logout 
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import JobForm
from datetime import date
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from io import BytesIO
from django.http import HttpResponse


def job_posting_chart(request):
    recruiters = Recruiter.objects.all()
    company_names = [recruiter.company for recruiter in recruiters] 
    job_counts = [Jobs.objects.filter(recruiter=recruiter).count() for recruiter in recruiters]

    fig, ax = plt.subplots()
    ax.bar(company_names, job_counts, color='red')
    ax.set_xlabel('Company')
    ax.set_ylabel('Number of Jobs Posted')
    ax.set_title('Number of Jobs Posted by Each Company')

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    return HttpResponse(buf.getvalue(), content_type='image/png')


def job_application_percentage_chart(request):
    jobs = Jobs.objects.all()
    job_titles = [job.job_title for job in jobs]
    application_counts = [Apply.objects.filter(job=job).count() for job in jobs]

    
    if sum(application_counts) == 0:
        return HttpResponse("No applications available to generate chart.", content_type="text/plain")
    fig, ax = plt.subplots()
    ax.pie(application_counts, labels=job_titles, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    ax.axis('equal')  
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    return HttpResponse(buf.getvalue(), content_type='image/png')



def index(request):
   data = Jobs.objects.all().order_by('-start_date')[:4] 
   return render(request,'index.html',{'data':data})


def search(request):
    if request.method == 'GET':
        search_query = request.GET.get('search', '')
        location_query = request.GET.get('location', '')
        
        if search_query and location_query:
            jobs = Jobs.objects.filter( job_title__icontains=search_query, location__icontains=location_query)
        elif search_query:
            jobs = Jobs.objects.filter( job_title__icontains=search_query)
        elif location_query:
            jobs = Jobs.objects.filter(location__icontains=location_query)
        else:
            jobs = []
            
        return render(request,'search.html', {'search_query': search_query, 'location_query': location_query, 'data': jobs})


def letest_job(request):
    data=Jobs.objects.all().order_by('-start_date') 
    return render(request,'latest_jobs.html',{'data':data})


def contact_us(request):
    return render(request ,'contact.html')



# User views......................................
@login_required(login_url='user_login')  
def user_home(request):
    data = Jobs.objects.all().order_by('?')
    user = request.user
    student = StudentUser.objects.get(user=user)
    applied = Apply.objects.filter(student=student)
    li = []
    for application in applied:
        li.append(application.job.id) 
    return render(request, 'User/user_home.html',{'data':data,'li':li})


# --------------User Signup---------------------#
def Usersignup(request):
    error=''
    if request.method == 'POST':
       f = request.POST['first']
       l = request.POST['last']
       c = request.POST['contact']
       e = request.POST['email']
       p = request.POST['pwd']
       cp= request.POST['cpwd']
       g = request.POST['gender']
       i = request.FILES['img']
       try:
           user=User.objects.create_user(first_name=f,last_name=l,username=e,password=p)
           StudentUser.objects.create(user=user,mobile=c,image=i,gender=g,type="student")
           error='no'
       except:   
           error="yes"
              
    return render(request,'User/user_signup.html',{'error':error})
# ----------------End User Signup--------------------------#


# -------------------User Login-----------------------------#
def UserLogin(request):
    if request.method == "POST":
        email=request.POST['email']
        password =request.POST['password']
        user = authenticate(username=email,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request, 'Invalid username or password')
            
        
    return render(request,'User/user_login.html')

# ---------------------User Login End------------------------------#


# -------------------------View User-------------------------------#
def view_user(request):
    data = StudentUser.objects.all()
    return render(request,'User/view_user.html',{'data':data})


def user_latest_job(request):
    data = Jobs.objects.all().order_by('-start_date') 
    user = request.user
    student = StudentUser.objects.get(user=user)
    applied = Apply.objects.filter(student=student)
    li = []
    for application in applied:
        li.append(application.job.id)  # Assuming the Apply model has a 'job' foreign key to Jobs
    return render(request, 'User/user_job_list.html', {'data': data, 'li': li})


def Condidate_apply(request):
    data = Apply.objects.all()
    return render(request,'User/candidate_apply.html',{'data':data})


def job_details(request,id):
    data = Jobs.objects.get(id=id)
    return render(request,'User/job_details.html',{'data':data})

def apply_for_job(request,id):
    user = request.user
    student = StudentUser.objects.get(user=user)  # Get the student user
    job = Jobs.objects.get(id=id)  # Get the job by ID
    date1 = date.today()  # Get the current date
    if job.end_date < date1:
        messages.error(request, 'Application Closed')
    elif job.start_date > date1:
        messages.info(request, "Application Not Started")
    else:
        if request.method == 'POST':
            if 'resume' in request.FILES: 
                resume_file = request.FILES['resume']
                # Create and save the application
                Apply.objects.create(job=job,student=student,resume=resume_file,applydate=date1)
                messages.success(request, 'Job Applied Successfully')
            else:
                messages.error(request, 'Please upload a resume.')

    return render(request, 'User/apply_for_job.html', {'job': job})

    


def UserDelete(request,id):
    data = StudentUser.objects.get(id=id)
    data.delete()
    return redirect('view_user')


def User_profile(request):
    user = request.user 
    profiledata = StudentUser.objects.get(user=user)
    return render(request,'User/user_profile.html', {'user': user, 'profiledata': profiledata})

def edit_user_profile(request):
    user = request.user
    profiledata = StudentUser.objects.get(user=user)
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.username = request.POST.get('username')
        user.save()
        
        profiledata.mobile = request.POST.get('mobile')
        profiledata.gender = request.POST.get('gender')
        if 'image' in request.FILES:
            profiledata.image = request.FILES['image']
        profiledata.save()
        return redirect('userprofile')  
    return render(request, 'User/profile_edit.html', {'profiledata': profiledata})
# --------------------End View User-------------------------------#

# ---------------------Change User Password---------------------------#
def ChangeUserPassword(request):
    if request.method == 'POST':
        current_password = request.POST['cupass']
        new_password = request.POST['npass']
        confirm_password = request.POST['cpass']

        if new_password != confirm_password:
            messages.error(request, 'New password and confirmation password do not match.')
            return render(request, 'User/User_change_password.html')

        try:
           student_user = StudentUser.objects.get(user=request.user) 
           user = student_user.user  
           if user.check_password(current_password):
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password has been changed successfully!')
                return redirect('home')
           else:
                messages.error(request, 'Current password is incorrect.')
        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {str(e)}')

    return render(request, 'User/User_change_password.html')


#--------------------------------End User Password------------------------#


# ------------------------------------------------------------------#



# ============================Recuiter Views===========================#

# ---------------------Recuiter Home-------------------------#
def recuiter_home(request):
    return render(request,'Recruiter/recuiter_home.html')

# --------------------End Recuiter Home----------------------#


# -------------------Recuiter Singup--------------------------#
def RecruiterSignup(request):
    if request.method == 'POST':
        try:
           first= request.POST['first']
           last= request.POST['last']
           contact= request.POST['contact']
           company = request.POST['company']
           caddress = request.POST['caddress']
           industry = request.POST['industry']
           email1 = request.POST['email']
           cpwd = request.POST['cpwd']
           img = request.FILES['img']
           user=User.objects.create_user(first_name=first,last_name=last,username=email1,password=cpwd)
           saved = Recruiter(user=user,mobile=contact,company=company,company_address=caddress,industry=industry,image=img ,type="Recruiter" ,status="Pending")
           saved.save()  
           messages.success(request, 'Recruiter account created successfully!')
           return redirect('recruiter')  
       
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')
            return render(request, 'recruiter_login.html') 
    return render(request, 'Recruiter/recruiter_signup.html')
# ------------------------Recuiter signup end--------------------------#


# --------------------------Recuiter Login-----------------------------#
def RecruiterLogin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user:
            try:
                user1 = Recruiter.objects.get(user=user)
                if user1.type == "Recruiter" and user1.status != "Pending":
                    login(request, user)
                    return redirect('recruiter_home')  
                else:
                    messages.error(request, 'Recruiter status is Pending.')  
            except Recruiter.DoesNotExist:
                messages.error(request, 'Recruiter not found.')
        else:
            messages.error(request, 'Invalid username or password.')
            
    return render(request, 'Recruiter/recruiter_login.html')
# -------------------------End Recuiter Login-------------------------#
def RecuiterNavbar(request):
    return render(request,'Recruiter/recuiter_navbar.html')

def RecuiterPennding(request):
    data = Recruiter.objects.filter(status="Pending")
    return render(request ,'Recruiter/recruiter_pendding.html',{'data':data})

def RecuiterAccepted(request):
    data = Recruiter.objects.filter(status="Accepted")
    return render(request ,'Recruiter/accepted.html',{'data':data})

def RecuiterRejected(request):
    data = Recruiter.objects.filter(status="Rejected")
    return render(request ,'Recruiter/accepted.html',{'data':data})


def AllRecuiter(request):
    data = Recruiter.objects.all
    return render(request ,'Recruiter/allRecuiter.html',{'data':data})

def ChangeStatus(request,id):
    data=Recruiter.objects.get(id=id)
    if request.method == 'POST':
        s =request.POST['status']
        data.status=s
        data.save()
        return redirect('RecuiterPendding')
    return render(request,'Recruiter/change_status.html',{'data':data})


def Recruiter_profile(request):
    user = request.user 
    profiledata = Recruiter.objects.get(user=user)
    return render(request,'Recruiter/recruiter_profile.html', {'user': user, 'profiledata': profiledata})

def edit_recruiter_profile(request):
    user = request.user
    profiledata = Recruiter.objects.get(user=user)
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.username = request.POST.get('username')
        user.save()
        
        profiledata.mobile = request.POST.get('mobile')
        profiledata.company_address = request.POST.get('company_address')
        if 'image' in request.FILES:
            profiledata.image = request.FILES['image']
        profiledata.save()
        return redirect('recuiterProfile')  
    return render(request, 'Recruiter/edit_profile.html', {'profiledata': profiledata})


def RecuiterChangePassword(request):
    if request.method == 'POST':
        current_password = request.POST['cupass']
        new_password = request.POST['npass']
        confirm_password = request.POST['cpass']

        if new_password != confirm_password:
            messages.error(request, 'New password and confirmation password do not match.')
            return render(request, 'Recruiter/recruiter_change_pass.html')

        try:
            recuiter_user = Recruiter.objects.get(user=request.user)
            user=recuiter_user.user
            if user.check_password(current_password):
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password has been changed successfully!')
                return redirect('recruiter')
            else:
                messages.error(request, 'Current password is incorrect.')
        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {str(e)}')

    return render(request,'Recruiter/recruiter_change_pass.html')

def add_job(request):
    fm=JobForm()
    if request.method == 'POST':
        fm = JobForm(request.POST , request.FILES)
        if fm.is_valid():
            recruiter = Recruiter.objects.get(user=request.user)
            job_title=fm.cleaned_data['job_title']
            start_date=fm.cleaned_data['start_date']
            end_date=fm.cleaned_data['end_date']
            job_salary=fm.cleaned_data['job_salary']
            image=fm.cleaned_data['image']
            description=fm.cleaned_data['description']
            experience=fm.cleaned_data['experience']
            location=fm.cleaned_data['location']
            skill=fm.cleaned_data['skill']
            created_date=fm.cleaned_data['created_date']
            saved = Jobs(recruiter=recruiter,job_title=job_title,start_date=start_date,end_date=end_date,job_salary=job_salary,image=image,description=description,experience=experience,location=location,skill=skill,created_date=created_date)
            saved.save()
            return redirect('job_list')
        else:
            fm=JobForm()  
    return render(request, 'Recruiter/add_job.html',{'fm':fm})
    
    
def jobList(request):
    user=request.user
    recruiter=Recruiter.objects.get(user=user)
    job=Jobs.objects.filter(recruiter=recruiter)
    return render(request,'Recruiter/job_list.html',{'job':job})

def JobDelete(request,id):
    data = Jobs.objects.filter(id=id)
    data.delete()
    return redirect('job_list')

def JobUpdate(request, id):
    pi = Jobs.objects.get(id=id) 
    if request.method == 'POST':
        fm = JobForm(request.POST, request.FILES, instance=pi)  
        if fm.is_valid():
            fm.save() 
            return redirect('job_list')
        else:
            messages.error(request, "Error updating job. Please correct the form.")
    else:
        fm = JobForm(instance=pi)  

    return render(request, 'Recruiter/Job_update.html', {'fm': fm})


# =======================Admin Home===============================#
@login_required(login_url='adminPage') 
def admin_home(request):
    
    requiter = Recruiter.objects.all().count()
    user = StudentUser.objects.all().count()
    
    return render(request,'Admin/admin_home.html',{'requiter':requiter,'user':user})

# ------------------Admin Login--------------------------#
def admin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user= authenticate(username=username,password=password)
        try:
          if user.is_staff:
            login(request,user)
            return redirect("admin_home")
        except:
                messages.error(request, 'Username and password does not match')
    return render(request,'Admin/admin_login.html')
# -------------------------End Admin login---------------------------#

# ---------------------Change Admin Password---------------------------#
def ChangeAdminPassword(request):
    if request.method == 'POST':
        current_password = request.POST['cupass']
        new_password = request.POST['npass']
        confirm_password = request.POST['cpass']

        if new_password != confirm_password:
            messages.error(request, 'New password and confirmation password do not match.')
            return render(request, 'Admin/admin_change_password.html')

        try:
            user = User.objects.get(id=request.user.id)
            if user.check_password(current_password):
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password has been changed successfully!')
                return redirect('admin_home')
            else:
                messages.error(request, 'Current password is incorrect.')
        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {str(e)}')

    return render(request, 'Admin/admin_change_password.html')


#--------------------------------End Admin Password------------------------#


def userLogout(request):
    logout(request)
    return redirect('/')
    