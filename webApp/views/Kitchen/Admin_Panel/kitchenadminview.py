from django.shortcuts import redirect,render
from  webApp.models import *
from django.contrib import messages

def  ReviewPendingKitchens(request):

    pending_kitchens = Kitchen.objects.filter(status="pending")

    return render(request,"",context={'pending_kitchens':pending_kitchens})


def  ToggleKitchenStatus(request):
    if request.method == 'POST':   

        status = request.POST.get('status') or None 
        kitchen_id = request.POST.get('kitchen_id') or None 

        Kitchen.objects.filter(pk=kitchen_id).update(status=status)

        messages.success(request, 'Kitchen status updated successfully !')   
        return redirect(request.META.get('HTTP_REFERER'))

