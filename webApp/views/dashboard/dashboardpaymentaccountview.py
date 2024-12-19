from django.shortcuts import render,redirect, HttpResponseRedirect
from webApp.models import *
from django.contrib import messages
from django.core.paginator import Paginator
from geopy.geocoders import Nominatim
from django.http import JsonResponse
from django.contrib.auth.models import User,Permission,Group
from django.contrib.auth import logout
from webApp.templatetags.webApp_extras import user_role
import json
import secrets
import string
from webApp.views.Others.geocode_address import *
from webApp.utils import *
from  fcm_django.models  import FCMDevice
from  webApp.views.expo_notif_view  import send_push_message
from  webApp.views.Others.fcm_notifs  import  *


def AddPaymentAccountForm(request,add_button_clicked=None):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if 'PaymentAccounts'  in chk or request.user.is_superuser:
        re_render = False
        user_id = request.user.id

        context= {'re_render':re_render,'user_id':user_id}
        return render(request, 'dashboard/Payment_Accounts/add_account_form.html', context)
    else:
        return render(request, 'dashboard/permission_denied.html')



def AddPaymentAccount(request):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if 'PaymentAccounts'  in chk or request.user.is_superuser:
        if request.method == 'POST':
            
            account_owner_title = request.POST.get('account_owner_title') or None
            print("account_owner_title",account_owner_title)


            if account_owner_title is None:
                user_added_warning = 'Please enter owner title'  
                messages.warning(request, user_added_warning)
                return redirect(request.META.get('HTTP_REFERER'))
            

            account_iban = request.POST.get('account_iban') or None
            print("account_iban",account_iban)


            if account_iban is None:
                user_added_warning = 'Please enter IBAN'  
                messages.warning(request, user_added_warning)
                return redirect(request.META.get('HTTP_REFERER'))
            
            bank_name = request.POST.get('bank_name') or None
            print("bank_name",bank_name)


            if bank_name is None:
                user_added_warning = 'Please enter bank name'  
                messages.warning(request, user_added_warning)
                return redirect(request.META.get('HTTP_REFERER'))



            user_id = request.POST.get('user_id') or None
            print("user_id",user_id)



            payment_account_instance = Paymentaccounts.objects.create(user_id = user_id, account_title = account_owner_title, iban_number = account_iban, bank_name =bank_name)
            payment_account_instance.save()


            group_added_success = 'Account info added successfully !'  
            messages.success(request, group_added_success)
            
                
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'dashboard/permission_denied.html')
    


def EditPaymentAccountForm(request,id,add_button_clicked=None):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if 'PaymentAccounts'  in chk or request.user.is_superuser:
        re_render = False
        user_id = request.user.id
        payment_account_instance = Paymentaccounts.objects.filter(id = id).first()


        context= {
                're_render':re_render,
                'user_id':user_id,
                'payment_account_instance':payment_account_instance

                }
        return render(request, 'dashboard/Payment_Accounts/edit_account_form.html', context)
    else:
        return render(request, 'dashboard/permission_denied.html')






def EditPaymentAccount(request):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if 'PaymentAccounts'  in chk or request.user.is_superuser:
        if request.method == 'POST':
            
            account_owner_title = request.POST.get('account_owner_title') or None
            print("account_owner_title",account_owner_title)


            if account_owner_title is None:
                user_added_warning = 'Please enter owner title'  
                messages.warning(request, user_added_warning)
                return redirect(request.META.get('HTTP_REFERER'))
            

            account_iban = request.POST.get('account_iban') or None
            print("account_iban",account_iban)


            if account_iban is None:
                user_added_warning = 'Please enter owner title'  
                messages.warning(request, user_added_warning)
                return redirect(request.META.get('HTTP_REFERER'))
            

            bank_name = request.POST.get('bank_name') or None
            print("bank_name",bank_name)


            if bank_name is None:
                user_added_warning = 'Please enter bank name'  
                messages.warning(request, user_added_warning)
                return redirect(request.META.get('HTTP_REFERER'))



            user_id = request.POST.get('user_id') or None
            print("user_id",user_id)

            account_payment_id = request.POST.get('account_payment_id') or None
            print("account_payment_id",account_payment_id)

            



            payment_account_instance = Paymentaccounts.objects.filter(id=account_payment_id).first()
            print("check ", payment_account_instance)

            payment_account_instance.iban_number = account_iban
            payment_account_instance.account_title = account_owner_title

            payment_account_instance.bank_name= bank_name
            payment_account_instance.save()


            group_added_success = 'Account info updated successfully !'  
            messages.success(request, group_added_success)
            
                
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'dashboard/permission_denied.html')





def PaymentAccountList(request):  
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    
    if 'PaymentAccounts'  in chk or request.user.is_superuser:
     
    
        all_accounts = Paymentaccounts.objects.filter(user_id = request.user.id).exists()
        if not all_accounts:
            ven = "Not Found"
            
        else: 
            p = Paginator(Paymentaccounts.objects.filter(user_id = request.user.id).all().order_by('-id'),15)
            page = request.GET.get('page')
            ven = p.get_page(page) 
        context = {'ven':ven}
        return render(request, 'dashboard/Payment_Accounts/index.html', context)
    else:
        return render(request, 'dashboard/permission_denied.html')


def DeletePaymentAccount(request,id=None):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)

    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    
    if 'PaymentAccounts'  in chk or request.user.is_superuser:
    
        print("here for deleteing payment records record")
        payment_account_record_id = request.GET.get("payment_method_id")    
        print("payment_account_record_id", payment_account_record_id)
        payment_account_instance = Paymentaccounts.objects.filter(id=payment_account_record_id).first()
        payment_account_name = payment_account_instance.account_title

        payment_account_instance.delete() 
        print("record deleted Successfully!")
        data = {'payment_account_name':payment_account_name}
        return JsonResponse(data)
    else:
        return render(request, 'dashboard/permission_denied.html')
    

def AllPaymentAccountslist(request):  
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group) 

    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    
    if  "Accountant" in chk:
        all_payments_accounts = Paymentaccounts.objects.all().exists()
        if not all_payments_accounts:
            ven = "Not Found"
            
        else: 
            p = Paginator(Paymentaccounts.objects.all().order_by('-id'),15)
            page = request.GET.get('page')
            ven = p.get_page(page) 
        context = {'ven':ven}
        print("checking alpha list",ven)
        return render(request, 'dashboard/Payment_Accounts/all_payment_accounts_list.html', context)
    
    elif 'PaymentAccounts'  in chk:
        owner_ids = Kitchen.objects.filter(kitchen_admin=request.user.id).values_list('approved_owner_id', flat=True)
        print("owner_ids",owner_ids)    
        if not owner_ids:
            ven = "Not Found"   
        else: 
            #  i want all records whose user_id are in owner ids list 
            p = Paginator(Paymentaccounts.objects.filter( user_id__in = owner_ids  ).order_by('-id'),15)
            page = request.GET.get('page')
            ven = p.get_page(page) 
        context = {'ven':ven}
        print("checking alpha list",ven)

        return render(request, 'dashboard/Payment_Accounts/all_payment_accounts_list.html',context)
    
    elif request.user.is_superuser :
        all_payments_accounts = Paymentaccounts.objects.all().exists()
        if not all_payments_accounts:
            ven = "Not Found"
            
        else: 
            p = Paginator(Paymentaccounts.objects.all().order_by('-id'),15)
            page = request.GET.get('page')
            ven = p.get_page(page) 
        context = {'ven':ven}
        print("checking alpha list",ven)
        return render(request, 'dashboard/Payment_Accounts/all_payment_accounts_list.html', context)
    else:
        return render(request, 'dashboard/permission_denied.html')
    




# Search Payment Account
def  PaymentAccountCustomSearch(request): 
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if 'PaymentAccounts'  in chk or request.user.is_superuser:
        print("here in Payment Accounts custom search")
        payment_account_name = request.GET.get('Account Title') or None   
        print("payment_account_name", payment_account_name)
        if 'Accountant' in chk or request.user.is_superuser:
            searched_payment_account_exist = Paymentaccounts.objects.filter(account_title__icontains=payment_account_name).exists()
        else:
            searched_payment_account_exist = Paymentaccounts.objects.filter(account_title__icontains=payment_account_name).filter(user_id__in=list(Kitchen.objects.filter(approved_owner_id=request.user.id).values_list('pk',flat=True))).exists()

        if searched_payment_account_exist:    
            searched_payment_account = list(Paymentaccounts.objects.filter(account_title__icontains=payment_account_name).values()) 
            print("list of payment_account",searched_payment_account) 
            
            context = {'ven':  searched_payment_account}  
            return JsonResponse({"success": True,"response":context}) 
        else:  
            return JsonResponse({"success": False})
    else:
        return render(request, 'dashboard/permission_denied.html')
    


# Search MY Payment Account
def  MyPaymentAccountCustomSearch(request): 
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if 'PaymentAccounts'  in chk or request.user.is_superuser:
        print("here in MYYYYYYYY Payment Accounts custom search")
        payment_account_name = request.GET.get('Account Title') or None   
        print("payment_account_name", payment_account_name)
        
        searched_payment_account_exist = Paymentaccounts.objects.filter(account_title__icontains=payment_account_name).filter(user_id=request.user.id).exists()
        if searched_payment_account_exist:    
            searched_payment_account = list(Paymentaccounts.objects.filter(account_title__icontains=payment_account_name).filter(user_id=request.user.id).values()) 
            print("list of payment_account",searched_payment_account) 
            
            context = {'ven':  searched_payment_account}  
            return JsonResponse({"success": True,"response":context}) 
        else:  
            return JsonResponse({"success": False})
    else:
        return render(request, 'dashboard/permission_denied.html')
    



def KitchenPaymentShare(request):  
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group) 

    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    
    if 'Accountant' in chk:
        status_id_value = Orderstatus.objects.filter(is_pickup = True).first()
        order_ids_list = OrderProcessedStatuses.objects.filter(status_id= status_id_value.pk).values_list('order_id', flat=True)
        print("order_ids_list",order_ids_list)
        all_records = kitchenOrdersPayment.objects.all().exists()
        if not all_records:
            ven = "Not Found"
            
        else: 
            p = Paginator(kitchenOrdersPayment.objects.filter(order_id__in = order_ids_list).order_by('-id'),15)
            page = request.GET.get('page')
            ven = p.get_page(page) 
        context = {'ven':ven}
        print("checking alpha order records list",ven)
        return render(request, 'dashboard/Payment_Accounts/kitchen_payment_share.html', context)
    
    elif 'PaymentAccounts' in chk:
        kitchen_ids = Kitchen.objects.filter(kitchen_admin=request.user.id).values_list('id', flat=True)

        all_records = kitchenOrdersPayment.objects.all().exists()
        if not all_records:
            ven = "Not Found"
            
        else: 
            p = Paginator(kitchenOrdersPayment.objects.filter(Kitchen_id__in = kitchen_ids ).order_by('-id'),15)
            page = request.GET.get('page')
            ven = p.get_page(page) 
        context = {'ven':ven}
        print("checking alpha order records list",ven)
        return render(request, 'dashboard/Payment_Accounts/kitchen_payment_share.html', context)
    elif request.user.is_superuser:
        all_records = kitchenOrdersPayment.objects.all().exists()
        if not all_records:
            ven = "Not Found"
            
        else: 
            p = Paginator(kitchenOrdersPayment.objects.all().order_by('-id'),15)
            page = request.GET.get('page')
            ven = p.get_page(page) 
        context = {'ven':ven}
        print("checking alpha order records list",ven)
        return render(request, 'dashboard/Payment_Accounts/kitchen_payment_share.html', context)
    
    else:
        return render(request, 'dashboard/permission_denied.html')


def UpdateKitchenPaymentShareStatus(request):
    
    
    payment_record_id = request.GET.get("record_id")
    print('payment_record_id',payment_record_id)
    payment_record_instance = kitchenOrdersPayment.objects.filter(pk=payment_record_id).first()
    payment_record_instance.status = "Paid"
    payment_record_instance.save()
    
    kitchen_instance = Kitchen.objects.filter(id= payment_record_instance.Kitchen_id).first()
    print("kitchen instance",kitchen_instance.pk)
    if  FCMDevice.objects.filter(user_id= kitchen_instance.approved_owner.pk).filter(active=True).exists():
        fcm_device_instance = FCMDevice.objects.filter(user_id= kitchen_instance.approved_owner.pk).filter(active=True)
        for  device  in fcm_device_instance:
            token = device.registration_id
            print("token",token)  
            message = 'Funds Transferred for Your Cooking Services'
            try: 
                # token = 'ExponentPushToken[TaigETFvKvM4F_0vGKGlD8]'
                
                # # if Daily Order
                # if  OrderItems.objects.filter(order_id = Order_instance.pk).exists():
                #     extra = {"link": "/(tabs)/daily_orders"}
                # else:
                #     # if Menu Order 
                #     extra = {"link": "/(tabs)/other_orders"}
                extra = {"link": "/(tabs)/home/" + str(kitchen_instance.pk)}
                send_push_message(token, message, extra)
                print("messaged sent")
            except:
                print("kitchen payment paid messaged not  sent to app device",device.registration_id)
                try:
                    send_kitchen_notification_fcmi({"registration_tokens":[token],"id": payment_record_instance.order_id,"text":"the order number is" + str(payment_record_instance.order_id),"title":  message,'orders':[payment_record_instance.order_id],"session_image":"https://relatable-bucket.s3.amazonaws.com/static/session_images/PointingAarowInward.png"})
                except Exception as ee:
                    print("kitchen payment paid messaged not  sent to kitchen web",ee)

    else:
        print("messaged not  sent no active device for kitchen")

    data = {'resp_message': "Payment record status updated"}
    return JsonResponse(data) 







def KitchenAccountsDetaillist(request,id):  
    
    print('id',id)
    kitchen_instance = Kitchen.objects.filter(id= id).first()
    print('kitchen_instance',kitchen_instance.pk)
    owner_id = kitchen_instance.approved_owner_id
    print('owner_id',owner_id)
    
    all_payments_accounts = Paymentaccounts.objects.filter(user_id = owner_id).exists()
    if not all_payments_accounts:
        ven = "Not Found"
        
    else: 
        p = Paginator(Paymentaccounts.objects.filter(user_id = owner_id).order_by('-id'),15)
        page = request.GET.get('page')
        ven = p.get_page(page) 
    context = {'ven':ven}
    print("checking alpha list",ven)
    return render(request, 'dashboard/Payment_Accounts/kitchen_accounts_detail.html', context)
    