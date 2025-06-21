from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth . models import User


def signup(request) :
    if request.method == 'POST' :
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if username == '' or password == '':
            messages.error(request, 'Please fill the required fields')
            return redirect('/')
        elif password != password2 :
            messages.error(request, 'Password doesn\'t match!')
            return redirect('sign-up')
        elif password == password2 :
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return redirect('/')
    else : 
        return render(request, 'signup.html')

@never_cache  
def login(request) :
    if 'username' in request.session:
        return redirect('home')

    if request.method == 'POST':
         username = request.POST['username']
         password = request.POST['password']
         user = authenticate(username=username,password=password)
         
         if user is not None:
            if user.is_superuser:
               messages.error(request,'Admin has no permission to login in user page')
               return redirect('/')
            else :
                request.session['username'] = username
                return redirect('home')
         else:
            messages.error(request,'invalid username or password')
            return redirect('/')
    else:
        return render(request,'login.html')

@never_cache    
def home(request) :
    if 'username' in request.session:
        return render(request,'home.html')
        
    return redirect('/')

    
@never_cache  
def logout(request) :
    if 'username' in request.session:
        request.session.flush()
    return redirect('/')
    

