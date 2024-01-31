from django.shortcuts import render,redirect

def Index(request):
    return render(request,'index.html')

def About(request):
    return render(request,'about.html')

def Services(request):
    return render(request,'services.html')

def Contact(request):
    return render(request,'contact.html')

# def test(request):

#     from bus_reserve.models import TicketOrder

#     orders = TicketOrder.objects.filter(user_id__email=request.user.email,\
#                                         ticket_id__schedule_id='22724fda-0226-4593-b46f-eac8f67c66b7')\
#                                             .order_by('-bought_date')[0]

#     return render(request, 'account/ticket.html', {'context':orders})

        
