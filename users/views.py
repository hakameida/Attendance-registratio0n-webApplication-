from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile,Session
from .forms import sessionForm,messageForm,UserForm,ProfileForm
from django.core.mail import send_mail, BadHeaderError
import pickle
import os  
from keras_facenet import FaceNet
from ultralytics import YOLO 
from .finalproject import facereco
from .makePkl import makePkl
model=FaceNet(key="20180402-114759",cache_folder=r"C:\Users\Administrator\Desktop\projectweb\smartface\Face-Recognition-with-FaceNET-main")
model_yolo= YOLO(r"C:\Users\Administrator\Desktop\projectweb\smartface\yolov8n-face.pt")

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
            
        except:
            messages.error(request,'email does not exist') 

        user=authenticate(request,username=username,password=password)
        if user is not None:
            ss=user.profile
            # ss = request.User.profile
            print(ss)
            if ss.super: 
                login(request,user)
                return redirect('sessions')
            else:
                login(request,user)
                return redirect('account')

        else :
            messages.error(request,"username or password not correct")
    return render(request,'users/login_register.html')


def logoutUser(request):
    logout(request)
    messages.error(request,"user was logged out!")
    return redirect('login')

def index(request):
    return render(request,'index.html') 
def about(request):
    return render(request,'users/about.html')

def account(request):
    Profile=request.user.profile
    context={'Profile':Profile}
    return render(request,'users/account.html',context) 

@login_required(login_url='login')
def createsession(request):
    ss = request.user.profile
    
    if ss.super:
        form = sessionForm()
        
        if request.method == 'POST':
            form = sessionForm(request.POST, request.FILES) 
            if form.is_valid():
                session = form.save()
                profiles = Profile.objects.all()
                
                # Sending email to all profiles
                email_subject = "New Session Announcement"
                email_message = f"A new session '{session.session_name}' has been created. Please check it out."
                recipient_list = [profile.email for profile in profiles]
                print(recipient_list)
                sender_email = "computervision188@gmail.com"  # Update with your actual sender email address
                
                # try:
                #     send_mail(email_subject, email_message, sender_email, recipient_list, fail_silently=False)
                # except BadHeaderError:
                #          return render(request, '500.html', {'message': 'Invalid header found.'})
                # except Exception as e:
                #           return render(request, '500.html', {'message': str(e)})
                
                return redirect('sessions')
        
        context = {'form': form} 
        return render(request, 'users/add_session.html', context) 


@login_required(login_url='login')
def sessions(request):
    sessions=Session.objects.all()
    context={'sessions':sessions}
    return render(request,'users/sessions.html',context) 


@login_required(login_url='login')
def updatesession(request, pk):
    session = Session.objects.get(id=pk)
    form = sessionForm(instance=session)
    if request.method == 'POST':
        form = sessionForm(request.POST, request.FILES, instance=session)
        if form.is_valid(): 
            saved = form.save(commit=False) 
            saved=form.save()
            id_image = {}
            for profile in Profile.objects.all():
                      id_image[profile.id] = 'static/images/' + profile.image.name if profile.image else None
            print(id_image) 
            if   saved.image_self:
                 image = saved.image_self 
                 my_path = "static/images/"
                 new_dir = str(image)
                 path_of_image= os.path.join(my_path, new_dir)  
                 print(path_of_image)
                 filename = "data4.pkl"
                 directory = r"C:\Users\mreid\Desktop\projectweb\smartface"
                 if os.path.isfile(os.path.join(directory, filename)):
                        student_count = Profile.objects.filter(super=False).count()
                        myfile = open(r"C:\Users\mreid\Desktop\projectweb\smartface\data4.pkl", "rb")
                        data = pickle.load(myfile)
                        
                        if student_count == len(data) :
                           id_attendance= facereco(path_of_image,model,model_yolo)
                        else:
                           profile = Profile.objects.filter(user=None).first()

                           if profile :
    
                            profile.delete()
                           makePkl(id_image,model,model_yolo)  
                           id_attendance=facereco(path_of_image,model,model_yolo)
                 else:
                        profile = Profile.objects.filter(user=None).first()

                        if profile :
    
                           profile.delete()
                        makePkl(id_image,model,model_yolo)
                        id_attendance=facereco(path_of_image,model,model_yolo)
                 print(id_attendance)
                 profiles = Profile.objects.filter(id__in=id_attendance)
                 profile_ids = profiles.values_list('id', flat=True) 
                 profiless = Profile.objects.filter(id__in=profile_ids) 
                 try:  
                      session.profile.add(*profiles)
                      print(session.profile.all())
                 except Exception as e:
                       print('Error adding profiles to session:', e) 
                 try:
                       session = form.save(commit=False)  # Save the Session instance without committing to the database
                       session.profile.set(profiless)  # Set the many-to-many relationship between the Session and Profile models
                       session.save()  # Commit the Session instance to the database
                       print('Session saved')
                 except Exception as e:
                        print('Error saving session:', e)
                        print(e)
                #  email_subject = "New Session Announcement"
                #  email_message = f"Dear {', '.join(profiles)},\n\nA new session has been added. Please check it out."
                #  recipient_list = [profile.email for profile in profiles]
                #  sender_email = "your-email@example.com"  # Update with your actual sender email address
                #  send_mail(email_subject, email_message, sender_email, recipient_list)

                 return redirect('sessions')
        else:
               print(form.errors)
    context = {'form': form}
    return render(request, 'users/add_session.html', context)


@login_required(login_url='login')
def deletesession(request, pk):
    session=Session.objects.get(id=pk) 
    if (request.method=='POST'):
        session.delete() 
        return redirect('sessions')
    context={'object':session} 
    return render(request,'users/delete_session.html',context) 


login_required(login_url='login') 
def inbox(request):
    profile=request.user.profile
    messageRequests= profile.messages.all()
    unreadCount=messageRequests.filter(is_read=False).count()
    context={'messageRequests':messageRequests,'unreadCount':unreadCount}
    return render(request,'users/inbox.html',context) 


login_required(login_url='login') 
def viewmessage(request,pk):
    profile=request.user.profile 
    message=profile.messages.get(id=pk)  
    if message.is_read==False:
      message.is_read=True
      message.save()
    context={'message':message} 
    return render(request,'users/message.html',context) 




def createmessage(request,pk):
    recipient=Profile.objects.get(id=pk)
    form=messageForm()
    try:
        sender=request.user.profile
    except:
        sender=None    
    if request.method=='POST':
        form =messageForm(request.POST)
        if form.is_valid():
           message=form.save(commit=False)
           message.sender=sender
           message.recipient=recipient
           if sender:
               message.name=sender.name
               message.email=sender.email
           message.save()
           messages.success(request,'your message was successfully sent!')
           return redirect('contact')
    context={'recipient':recipient,'form':form}
    return render(request,'users/message_form.html',context) 


def contact(request):
    profiles=Profile.objects.all()
    context={'profiles':profiles}
    return render(request,'users/contact.html',context)  
       


def sessionsstudent(request): 
    sessions = request.user.profile.sessions.all()
    sessionsme = sessions.count()
    profile_name = request.user.profile.name 
    sessionss = Session.objects.all()
    sessionsall = sessionss.count() 
    sessions_not_in_profile = sessionss.exclude(id__in=sessions.values_list('id', flat=True)) 
    attendance = (sessions.count() / Session.objects.all().count()) * 100

    context = {'profile_name': profile_name, 'sessions': sessions, 'sessionss': sessionss,
             'sessionsall': sessionsall, 'sessionsme': sessionsme,'sessions_not_in_profile': sessions_not_in_profile
                  ,'attendance':attendance} 
    return render(request, 'users/session_student.html', context)


@login_required(login_url='login')
def signalsession(request,pk):
     session=Session.objects.get(id=pk)
     context={'session':session}
     return render(request,'users/signal_session.html',context) 

@login_required(login_url='login')
def show_profiles(request):
    profiles = Profile.objects.all()

    for profile in profiles:
        total_sessions = profile.sessions.count()
        attended_sessions = profile.sessions.filter(attendance=True).count()
        percentage = (attended_sessions / total_sessions) * 100 if total_sessions > 0 else 0
        profile.percentage_attendance = percentage

    context = {'profiles': profiles}
    return render(request, 'students_attendance.html', context)

def create_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            # Create or update the user object
            user = user_form.save(commit=False)
            password = user_form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # Create or update the profile object
            profile, created = Profile.objects.get_or_create(user=user)
            profile.username = user.username
            profile.email = user.email
            profile.name = user.first_name
            profile.super = profile_form.cleaned_data['super']
            profile.firstname = profile_form.cleaned_data['firstname']
            profile.secondname = profile_form.cleaned_data['secondname']
            profile.image = profile_form.cleaned_data['image']
            profile.save()

            messages.success(request, 'User added successfully')

            return redirect('create_profile')  # Replace with your desired redirect URL
    else:
        user_form = UserForm()
        profile_form = ProfileForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'users/create_profile.html', context)