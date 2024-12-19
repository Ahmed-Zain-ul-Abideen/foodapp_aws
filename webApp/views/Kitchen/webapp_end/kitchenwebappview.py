from  django.shortcuts import render,redirect
from django.contrib import messages
from webApp.models import *
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
import json

def   SaveKitchen(request):

    if request.method == 'POST':   

        name = request.POST.get('name') or None 
        owner = request.POST.get('owner') or None 
        contact = request.POST.get('contact') or None 
        email = request.POST.get('email') or None  

        kitchen_instance = Kitchen.objects.create(name=name,owner=owner,contact=contact,email=email)
        kitchen_instance.save()

        kitchen_speciality_items = request.POST.get('kitchen_speciality_items') or None 

        kitchen_speciality_instance = KitchenSpeciality.objects.create(kitchen_id=kitchen_instance.id,
            items=json.dumps(kitchen_speciality_items)
        )
        kitchen_speciality_instance.save()

        address_line1 = request.POST.get('address_line1') or None  
        address_line2 = request.POST.get('address_line2') or None  
        city = request.POST.get('city') or None  
        country = request.POST.get('country') or None  
        postal_code = request.POST.get('postal_code') or None  

        kitchen_address = KitchenAddress.objects.create(kitchen_id=kitchen_instance.id,address_line1=address_line1,
            address_line2=address_line2,city=city,country=country,postal_code=postal_code
        )
        kitchen_address.save() 

        kitchen_media_files_list = request.FILES.getlist('kitchen_media_files_list') or None
        if kitchen_media_files_list is not None:
            for file in kitchen_media_files_list:
                if file.content_type.startswith('image'): 
                    image = Image.open(file)
                    if image.mode in ("RGBA", "P"):
                        image = image.convert("RGB")
                    buffer = BytesIO()
                    image.save(buffer, format='JPEG', optimize=True, quality=98)
                    file = InMemoryUploadedFile(buffer, None, file.name, 'image/jpeg', buffer.getbuffer().nbytes, None) 

                kitchen_media_instance = KitchenMedia.objects.create(kitchen_id=kitchen_instance.id,file=file)
                kitchen_media_instance.save() 

        messages.success(request, 'Kitchen info saved successfully and pending approval !')   
        return redirect(request.META.get('HTTP_REFERER'))
