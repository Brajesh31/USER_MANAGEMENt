from django.shortcuts import render,redirect
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth . models import User, auth
from .forms import UserForm


# Create your views here

@never_cache  
def adminlogin(request) :
    if 'user' in request.session :
        return redirect('admin-home')

    if request.method == 'POST' :
         username = request.POST['user']
         password = request.POST['password']
         user = auth.authenticate(username=username,password=password)
         if user is not None :
            if user.is_superuser :
               request.session['user'] = username
               return redirect('admin-home')
            else:
                messages.error(request,'You are not an admin')
                return redirect('admin-login')
         else:
            messages.error(request,'invalid username or password')
            return redirect('admin-login')
    else:
         return render(request,'adminlogin.html')

@never_cache    
def adminhome(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    if 'user' in request.session:
        user = User.objects.filter(username__istartswith=q)
        return render(request,'adminhome.html',{'user':user})
        
    return redirect('admin-login')

 
@never_cache  
def adminlogout(request):
    if 'user' in request.session:
        request.session.flush()
    return redirect('admin-login')



def admindelete(request,id):
    user=User.objects.get(id=id)
    context = {'user' : user}
    if request.method == 'POST' :
        
        User.objects.filter(id=id).delete()
        
        return redirect('admin-home')
    return render(request, 'admindelete.html', context)



def adminupdate(request,id):
    user=User.objects.get(id=id)
    form = UserForm(instance=user)
    if request.method=='POST':
        """
        if User.objects.filter(username=username).exists() :
                messages.error(request, 'User Name already exists, Please register a new admin.')
                return redirect('adminregister')
        """
        form=UserForm(request.POST,instance=user)
        
        
        if form.is_valid() :
            form.save()
            return redirect('admin-home')
    context={'form':form}    
    return render (request,'adminupdate.html',context)
         
         
def adminregister(request) :
    if 'user' not in request.session :
        return redirect('adminlogin')
    
    if request.method == 'POST' :
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if username == '' or password == '' :
            messages.error(request, 'Please fill in the requered fields.')
            return redirect('adminregister')
        elif password != password2 :
            messages.error(request, 'Password is not matching. Try again!')
            return redirect('admin-register')
        elif password == password2 :
            
            # checking if the username is already exists
            if User.objects.filter(username=username).exists() :
                messages.error(request, 'User Name already exists, Please register a new admin.')
                return redirect('admin-register')
            else :
                
                # creating new user
                user = User.objects.create_user(username=username, password=password)
                user.save()
                return redirect('admin-home')
    else :
        return render(request, 'adminregister.html')