from django.shortcuts import render,redirect, HttpResponse
from django.views import View
from .models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import random
from .tasks import send_activation_email,send_mail_verify, send_refund_mail
from bus_reserve.models import *
 

class Signup(View): 
        
        def get(self, request, *args, **kwargs):
            return render(request,'account/signup.html')  

        def post(self, request, *args, **kwargs):       
            username=request.POST['username']
            phone = request.POST['number']
            email = request.POST['email']
            password = request.POST['password']
            address=request.POST['address']

            if User.objects.filter(email=email) or User.objects.filter(username=username):
               messages.error(request, "username already exits please try some others")
               return redirect('signup')
            else:
                my_user=User.objects.create_user(email=email,username=username,ph=phone,address=address)
                my_user.set_password(password)
                my_user.save()           
                uid=urlsafe_base64_encode(force_bytes(my_user.id))
                token=PasswordResetTokenGenerator().make_token(my_user)
                link='http://127.0.0.1:8000/user/verify/'+uid+'/'+token
                send_activation_email.delay(email,link)
                messages.success(request,"Please Verify your Account")
                return redirect('Login')
            
class VerifyUser(View):  
                      
  def get(self,request,id,token):
        id=force_str(urlsafe_base64_decode(id))
        if not id or not token:
            messages.warning(request,"Invalid Token Id") 
            return redirect('signup')
        user = User.objects.get(id=id)
        if default_token_generator.check_token(user, token):
            if user.is_active:
                messages.warning(request,"Account Already Verified") 
                return redirect('signup')
            user.is_active = True
            user.save()
            messages.success(request,"Account Verified Successfully")
            return redirect('Login')
        else:
            messages.warning(request,"Invalid Token Id") 
            return redirect('signup')



class Login(View):

    def get(self, request, *args, **kwargs):
        return render(request,'account/login.html') 
    
    def post(self, request, *args, **kwargs): 
             email = request.POST['email']
             password = request.POST['password']
             user=User.objects.get(email=email)
             if user.is_active:
              myuser = authenticate(email=email,password=password)
              if myuser is not None:
                if user.is_active:
                  login(request,myuser)
                  request.session['email'] =email
                  messages.success(request,"Login successfully")
                  return redirect('home')
                else:
                  messages.warning(request,"Activate Your Account")
                  return redirect('Login')
              else:
               messages.warning(request,"Password or Email donot match") 
               return redirect('Login')
             else:
                messages.success(request,"Please Verify your account")
                return redirect('Login')
                   
       
@method_decorator(login_required(login_url='Login'), name='dispatch')
class Logout(View):
   def get(self, request, *args, **kwargs):
     logout(request)
     return redirect('Login')
   
class ResetpasswordView(View):

    def get(self, request, *args, **kwargs):
       return render(request,'account/reset.html')
    
    def post(self,request):
        email = request.POST.get('email')

        if not User.objects.filter(email=email).exists():
            messages.warning(request,"Email donot match") 
            return redirect('reset')

        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token1 =  random.randint(1, 1000)
        user.tc=token1
        user.save()
        activation_url = 'http://127.0.0.1:8000/user/confirmreset/'+ uid + '/' 
        print(activation_url)
        send_mail_verify.delay(user.email,activation_url,token1)
        messages.success(request,"Please Verify your Token")
        return redirect('reset')

class Verifytoken(View):
      
      def get(self,request,id):
        id=force_str(urlsafe_base64_decode(id))
        if not id :
            messages.warning(request,"Invalid Token Id") 
            return redirect('signup')
        user = User.objects.get(id=id)
        return render(request,'account/token_verify.html')
      
      def post(self,request,id):
        id=force_str(urlsafe_base64_decode(id))
        print(id)
        user=User.objects.get(id=id)
        tk= int(request.POST.get('tk'))
        if user.tc == tk:
            user.tc=0
            user.save()
            messages.success(request,"Token Verified successfully")
            return render(request,'account/password_change.html',{'id':id})
        else:
            messages.warning(request,"Invalid Token")
            return redirect('reset')

class Changepassword(View):
    def post(self,request):
        id = int(request.POST.get('id'))
        password= request.POST.get('password')
        # if str(password)<5:
        #     messages.warning(request,"Password length must be greater than 5")
        #     return redirect('Login')
        print(id,password)
        user=User.objects.get(id=id)
        if user:
            user.set_password(password)
            user.save()
            messages.success(request,"Password Changed successfully")
            return redirect('Login')
        else:
            messages.warning(request,"Invalid Error")
            return redirect('Login')

@method_decorator(login_required(login_url='Login'), name='dispatch')
class MyOrder(View):
  def get(self, request, *args, **kwargs):
    user_id=request.user.id  
    ticket_orders = TicketHistory.objects.filter(user_id=user_id)
    pending_tickets = TicketOrder.objects.filter(user_id=user_id)
    return render(request,'account/Order.html',{'ticket_orders': ticket_orders, 'pending_tickets':pending_tickets})
  
  def post(self, request):
      
      tik_id = request.POST.get('tik_id')
      
      send_refund_mail.delay(tik_id)

      return HttpResponse("Refund request has been submitted")

@method_decorator(login_required(login_url='Login'), name='dispatch')  
class MyDetail(View):
    def get(self, request, *args, **kwargs):
        user=User.objects.get(id=request.user.id)
        return render(request,{'user':user})

@method_decorator(login_required(login_url='Login'), name='dispatch')   
class Change_password(View):
    def get(self, request, *args, **kwargs):
        return render(request,'account/reset_password.html')
    
    def post(self,request):
        password1=request.POST['password1']
        password2=request.POST['password2']
        password3=request.POST['password3']
        user=User.objects.get(id=request.user.id)
        print(user.password,password1,password2,password3)

        if not user.check_password(password1):
            messages.warning(request,"Old Password Not Matched")
            return redirect('change_password')
        
        if password3 !=password2:
            messages.warning(request,"Confirm Password Not Matched")
            return redirect('change_password')
        
        user.set_password(password2)
        user.save()

        updated_user = authenticate(request,email=user.email, password=password2)
        login(request,updated_user)

        messages.success(request,"Password Changed successfully")
        return redirect('home')

@method_decorator(login_required(login_url='Login'), name='dispatch')
class User_details(View):
    def get(self, request, *args, **kwargs):
        return render(request,'account/user_details.html')
    

@method_decorator(login_required(login_url='Login'), name='dispatch')    
class Edit_user(View):   
    def get(self, request, *args, **kwargs):
        return render(request,'account/edit_user.html') 
    
    def post(self,request):
        username=request.POST['username']
        email=request.POST['email']
        ph=request.POST['ph']
        address=request.POST['address']

        user=User.objects.get(id=request.user.id)

        user.username=username
        user.email=email
        user.ph=ph
        user.address=address

        user.save()
        messages.success(request,"Details Changed successfully")
        return redirect('home')








