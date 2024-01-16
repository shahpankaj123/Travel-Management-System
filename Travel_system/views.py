from django.shortcuts import render,redirect

def Index(request):
    return render(request,'index.html')

        
