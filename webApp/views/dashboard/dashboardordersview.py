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
from webApp.views.Others.fcm_notifs  import *
from webApp.utils import *
from django.shortcuts import get_object_or_404

def Orderlist(request):  
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group) 

    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    
    if 'Call Agent'  in chk:
        all_order_status_cod = Orderstatus.objects.filter((Q(is_cod=True) | Q(is_cancelled=True)) & Q(role='Call Agent'))
        print('all_order_status_cod',all_order_status_cod)
        all_order_status_online = Orderstatus.objects.filter((Q(is_cod=False) | Q(is_cancelled=True)) & Q(role='Call Agent'))
        print('all_order_status_online', all_order_status_online)
        new_order_count = Orders.objects.filter(to_be_confirmed = True).count()
        all_orders = Orders.objects.filter(to_be_confirmed = True).all().exists()
        if not all_orders:
            ven = "Not Found"
            
        else: 
            new_order_count = Orders.objects.filter(to_be_confirmed = True).count()
            p = Paginator(Orders.objects.filter(to_be_confirmed = True).all().order_by('-id'),15)
            page = request.GET.get('page')
            ven = p.get_page(page) 
        context = {'ven':ven,
                   'new_order_count':new_order_count,
                   'all_order_status':all_order_status_cod,
                   'all_order_status_online':all_order_status_online}
        print("checking alpha list",ven)
        return render(request, 'dashboard/Orders/index.html', context)

    elif 'Rider'  in chk:
        all_order_status = Orderstatus.objects.filter(role = 'Rider' ).all()
        all_orders = Orders.objects.all().exists()
        if not all_orders:
            ven = "Not Found"
            
        else: 
            p = Paginator(Orders.objects.exclude(status__in=['to_be_confirmed','Confirmed_COD','payment_recieved','In-process','Delivered']).order_by('-id'),15)
            page = request.GET.get('page')
            ven = p.get_page(page) 
        context = {'ven':ven,
                   'all_order_status':all_order_status}
        print("checking alpha list",ven)
        return render(request, 'dashboard/Orders/index.html', context) 
        
    
    elif request.user.is_superuser:
        all_order_status = Orderstatus.objects.all()
        all_orders = Orders.objects.all().exists()
        if not all_orders:
            ven = "Not Found"
            
        else: 
            p = Paginator(Orders.objects.all().order_by('-id'),15)
            page = request.GET.get('page')
            ven = p.get_page(page) 
        context = {'ven':ven,
                   'all_order_status':all_order_status}
        print("checking alpha list",ven)
        return render(request, 'dashboard/Orders/index.html', context)
    
    elif 'Orders' in chk:
        all_order_status = Orderstatus.objects.all()
        kitchen_ids = Kitchen.objects.filter(kitchen_admin=request.user.id).values_list('id', flat=True)
        print("kitchen_ids",kitchen_ids)    
        if not kitchen_ids:
            ven = "Not Found"        
        else: 
            p = Paginator(Orders.objects.filter(kitchen_id__in = kitchen_ids).order_by('-id'),15)
            page = request.GET.get('page')
            ven = p.get_page(page) 
        context = {'ven':ven,
                   'all_order_status':all_order_status}
        print("checking alpha list",ven)
        return render(request, 'dashboard/Orders/index.html',context)
        
    else:
        return render(request, 'dashboard/permission_denied.html')
         

def OrderDetail(request,id):

    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group) 

    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    
    if 'Orders'  in chk or request.user.is_superuser or 'Kitchen' in chk:
        print("alpha check 123 ")
        order_instance = Orders.objects.filter(id=id).first()
        single_order_flag = False
        menu_order_flag = False
        deal_order_flag = False
        

        # Fetch Order Items
        if OrderItems.objects.filter(order_id = id).exists():
            single_order_flag = True
            orderitem_instances = OrderItems.objects.filter(order_id=id)
            print("orderitem_instances", orderitem_instances)

            
            order_items = []
            for order_item in orderitem_instances:
                # Retrieve the corresponding Menuitem for each OrderItem
                item_instance = Menuitems.objects.filter(id=order_item.item.pk).first()
                if item_instance:
                    order_items.append(item_instance)
            
            print("order_items", order_items)
            
            

            context = {'order_items':order_items,
                    'single_order_flag':single_order_flag,
                    'menu_order_flag':menu_order_flag,
                    'deal_order_flag':deal_order_flag,
                    'order_instance':order_instance    
                    }
        else:
            order_items = None
        # Fetch Order Menus
        if OrderMenuItems.objects.filter(order_id = id).exists():
            menu_order_flag = True
            
            ordermenu_instances = OrderMenuItems.objects.filter(order_id=id)
            print("ordermenu_instances", ordermenu_instances)

            order_menus = []
            for ordermenu_item in ordermenu_instances:
                # Retrieve the corresponding Menu for each OrderMenuItem
                menu_instance = Menu.objects.filter(id=ordermenu_item.menu.pk).first()
                print("menu_instance",menu_instance)
                if menu_instance:
                    order_menus.append(menu_instance)
            
            print("order_menus", order_menus)
            
            # menu_items = json.decoder.JSONDecoder().decode(menu_instance.associated_items)
            # total_count = menu_instance.category.menu_count
            

            
            
            if order_items:

                context = {'order_menus':order_menus,
                           'order_items':order_items,
                    'single_order_flag':single_order_flag,
                    'menu_order_flag':menu_order_flag,
                    'deal_order_flag':deal_order_flag,
                    'order_instance':order_instance
                    
                    
                    }
            else:

                context = {'order_menus':order_menus,
                    'single_order_flag':single_order_flag,
                    'menu_order_flag':menu_order_flag,
                    'deal_order_flag':deal_order_flag,
                    'order_instance':order_instance
                    
                    
                    }
        else:
            order_menus = None


            
        # Fetch Orders Deals
        if OrderDealItems.objects.filter(order_id = id).exists():
            deal_order_flag = True
            orderdeal_instances = OrderDealItems.objects.filter(order_id=id)
            print("orderdeal_instances", orderdeal_instances)

            order_deals = []
            for orderdeal_item in orderdeal_instances:
                deal_instance = Deals.objects.filter(id=orderdeal_item.deal.pk).first()
                if deal_instance:
                    order_deals.append(deal_instance)
            
            print("order_deals", order_deals)
            
            
            if order_items and order_menus:
                print("taking this context")

                context = {'order_deals':order_deals, 
                           'order_items': order_items , 
                           'order_menus':order_menus,               
                    'single_order_flag':single_order_flag,
                    'menu_order_flag':menu_order_flag,
                    'deal_order_flag':deal_order_flag,
                    'order_instance':order_instance                    
                    
                    }
            elif order_menus:
                context = {'order_deals':order_deals, 
                           'order_menus': order_menus ,                
                    'single_order_flag':single_order_flag,
                    'menu_order_flag':menu_order_flag,
                    'deal_order_flag':deal_order_flag,
                    'order_instance':order_instance                    
                    
                    }
            elif  order_items:
                

                context = {'order_deals':order_deals, 
                           'order_items': order_items ,                
                    'single_order_flag':single_order_flag,
                    'menu_order_flag':menu_order_flag,
                    'deal_order_flag':deal_order_flag,
                    'order_instance':order_instance                    
                    
                    }

                
            else:
                context = {'order_deals':order_deals,                    
                    'single_order_flag':single_order_flag,
                    'menu_order_flag':menu_order_flag,
                    'deal_order_flag':deal_order_flag,
                    'order_instance':order_instance                    
                    
                    }



    
        return render(request, 'dashboard/Orders/order_detail.html',context)
    else:
        return render(request, 'dashboard/permission_denied.html')



from django.db.models import Q, Prefetch



def  OrderCustomSearch(request): 
    
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)
    print('chk', chk)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    all_order_status_list=[]
    all_order_status = Orderstatus.objects.filter(role = 'Call Agent' ).all()
    for item in all_order_status:
        all_order_status_list.append(item.status_title)

    print("list ",all_order_status_list)
    # Fetch all possible order statuses with their ordering_bit values
    order_statuses = Orderstatus.objects.all()


    
    if 'Orders'  in chk or request.user.is_superuser:
        print("in if")
        role_title = chk[1]
        print('role_title',role_title)
        
        
        print("here in order custom search")
        order = request.GET.get('order') or None   
        print("order", order)
        try:
            searched_order_exist = Orders.objects.filter(Q(customer_name__icontains=order) | Q(contact__icontains=order) |  Q(id__icontains=order)).exists()
            # searched_order_exist = Orders.objects.filter(id =order).exists()
            print("in try")
            if searched_order_exist:   
                print(" in if 2 check") 
                searched_orders = list(Orders.objects.filter(Q(customer_name__icontains=order) | Q(contact__icontains=order) |  Q(id__icontains=order)).values())
                print("searched_orders", searched_orders)
                # searched_orders = list(Orders.objects.filter(id =order).values()) 
                print("list of order",searched_orders) 
                
                context = {'ven':  searched_orders,
                            'role_title':role_title,
                            'all_order_status_list':all_order_status_list}  
                return JsonResponse({"success": True,"response":context}) 
            else:  
                return JsonResponse({"success": False})  
        except:  
                return JsonResponse({"success": False})
    else:
        return render(request, 'dashboard/permission_denied.html')


# my kitchen order search
def  MyKitchenOrderCustomSearch(request): 

    
    print("here in my kitchen order custom search")
    order = request.GET.get('order') or None   
    print("order", order)
    searched_order_exist = Orders.objects.filter(id =order).filter(kitchen_id__in = list(Kitchen.objects.filter(approved_owner_id=request.user.id).values_list('pk',flat=True))).exists()
    if searched_order_exist:    
        searched_orders = list(Orders.objects.filter(id =order).values()) 
        print("list of order",searched_orders) 
        
        context = {'ven':  searched_orders}  
        return JsonResponse({"success": True,"response":context}) 
    else:  
        return JsonResponse({"success": False})
    



def  confirmorderpayment(request):
    id = request.GET.get("order_id")
    if   Orders.objects.filter(pk=id).filter(status="payment_recieved").exists():
        Orders.objects.filter(pk=id).update(status="ready_for_pickup")
    else:
        Orders.objects.filter(pk=id).update(status="payment_recieved")
    data = {'success':True}
    return JsonResponse(data)


def PreviousOrderlist(request):  
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group) 

    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    
    if 'Call Agent'  in chk:
        all_orders = Orders.objects.all().exists()
        if not all_orders:
            ven = "Not Found"
            
        else: 
            p = Paginator(Orders.objects.exclude(to_be_confirmed = True).all().order_by('-id'),15)
            page = request.GET.get('page')
            ven = p.get_page(page) 
        context = {'ven':ven,
                   }
        print("checking alpha list",ven)
        return render(request, 'dashboard/Orders/previous_orders.html', context)
    
    
from webApp.views.Regex_setting import cleanhtml


def AddOrderNotesForm(request,id,add_button_clicked=None):
    order_instance = Orders.objects.filter(id= id).first()

    re_render = False

    
    context= {'re_render':re_render,'order_instance':order_instance}
    return render(request, 'dashboard/Orders/add_order_notes.html', context)


def AddOrderNote(request):
       
    order_id = request.POST.get('order_id')
    print("order_id",order_id)
 
    order_notes = request.POST.get('order_notes') or None
    print("order_notes",order_notes)

    if order_notes is None:
        user_added_warning = 'Please enter service description!'  
        messages.warning(request, user_added_warning)
        return redirect(request.META.get('HTTP_REFERER'))
    
    if order_notes:
            order_notes = cleanhtml(order_notes)

    order_instance = Orders.objects.filter(id= order_id).first()
    order_instance.extra_notes = order_notes
    order_instance.save()
    
    item_added_success = 'Order note added successfully !'  
    messages.success(request, item_added_success)
    
        
    return redirect(request.META.get('HTTP_REFERER'))




def PendingRiderOrderlist(request):  
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group) 

    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    
    if 'Call Agent'  in chk:
        all_rider_list = RiderDetails.objects.all()
        all_orders = Orders.objects.all().exists()
        if not all_orders:
            ven = "Not Found"
            
        else: 
            p = Paginator(Orders.objects.filter(rider_pending= True).all().order_by('-id'),15)
            page = request.GET.get('page')
            ven = p.get_page(page) 
        context = {'ven':ven,'all_rider_list': all_rider_list
                   }
        print("checking alpha list",ven)
        return render(request, 'dashboard/Orders/rider_pending_orders_list.html', context)
    



def EditOrderStatusNotif(request):

    if request.method == 'POST':

        status_id = request.POST.get("status_id")
        print("status_id", status_id)
        order_id = request.POST.get("ven_id")
        print("order_id", order_id)
    
        

        if Orders.objects.filter(id = order_id).exists() and Orderstatus.objects.filter(id = status_id).exists():
            last_one  = "no"
            if  (Orders.objects.filter(to_be_confirmed= True).count())  == 1:
                last_one = "yes"
            status_instance = Orderstatus.objects.filter(id=status_id).first()
            Order_instance = Orders.objects.filter(id=order_id).first()

            Order_instance.status = status_instance.status_title
            Order_instance.to_be_confirmed = False
            
            # Start Send Push Notification to Register Kitchen Owner on Order Confirmation by Call Agent
            if  status_instance.is_cancelled == True:
                Order_instance.is_cancelled = True
            else:
                pass
    
            Order_instance.save()
            # if status_instance.status_title == "Confirmed_COD" or status_instance.status_title == "payment_recieved":
                
                # send notification
            kitchen_instance = Kitchen.objects.filter(id= Order_instance.kitchen.pk).first()
            print("kitchen instance",kitchen_instance.pk)
            if  FCMDevice.objects.filter(user_id= kitchen_instance.approved_owner.pk).filter(active=True).exists():
                fcm_device_instance = FCMDevice.objects.filter(user_id= kitchen_instance.approved_owner.pk).filter(active=True)
                for  device  in fcm_device_instance:  
                    try:
                        token = device.registration_id
                        print("token",token)

                    
                        # token = 'ExponentPushToken[TaigETFvKvM4F_0vGKGlD8]'
                        message = 'Get Ready to Cook! New Order recently assigned to your kitchen'
                        # if Daily Order
                        if  OrderItems.objects.filter(order_id = Order_instance.pk).exists():
                            extra = {"link": "/(tabs)/daily_orders"}
                        else:
                            # if Menu Order 
                            extra = {"link": "/(tabs)/other_orders"}
                        send_push_message(token, message, extra)
                        print("messaged sent")
                    except:
                        print("messaged not  sent to device",device.registration_id)

            else:
                print("messaged not  sent no active device for kitchen")

            # else:
            #     print("inelse")
            #     pass

            # End Send Push Notification to Register Kitchen Owner on Order Confirmation by Call Agent

            # Start Push Notification customer app
            

            cos_token = Order_instance.order_fcm
            # cos_token = 'ExponentPushToken[CmDGosEnqa3AZbocygQ_vy]'
            
            if status_instance.is_cancelled == True:
                cos_message = 'Your order is canceled!'
            else:
                cos_message = 'Your order is confirmed! We are on it and processing it now.'

            extra = {"link": "/(tabs)/Orders/singleOrder"}
            send_push_message(cos_token, cos_message,extra)
            print("messaged sent")

            

            #  End Push Notification customer app
            data = {'status': 'success', 'message': 'Status updated successfully!','last_one':last_one}
        else:
            data = {'status': 'error', 'message': 'Order or Status not found'}
        
        return JsonResponse(data)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

from webApp.views.expo_notif_view import send_push_message,send_salient_data_message

# Forcely assign rider to pending orders
def AssignRiderPendingOrders(request):

    if request.method == 'POST':

        rider_id = request.POST.get("rider_id")
        print("rider_id", rider_id)
        order_id = request.POST.get("ven_id")
        print("order_id", order_id)
    
        

        if Orders.objects.filter(id = order_id).exists() and RiderDetails.objects.filter(id = rider_id).exists():
            if  Orders.objects.filter(id=order_id).filter(rider_pending=True).exists():
                # Orders.objects.filter(id=order_id).update(rider_pending=False)

                kitchen_info = KitchenAddress.objects.filter(Kitchen_id__in= list(Orders.objects.filter(pk=order_id).values_list('kitchen_id',flat=True))).first()
                 
                rider, the_distance = lat_long_forced_rider(kitchen_info.latitude,kitchen_info.longitude,rider_id)
                print("rider for notif scedule",rider,' the_distance',the_distance)
                if  rider  is  None:
                    data = {'status': 'error', 'message': 'This rider cannot be assigned'}
                else:
                    order_rads = Orders.objects.filter(pk=order_id).first()
                    the_distance  =  float(the_distance)  +   float(order_rads.kitchen_to_customer_distance)
                    print("delivery_distance",the_distance)
                    # the_distance  =  the_distance  +  distance_in_km(order_rads.latitude,order_rads.longitude,kitchen_info.latitude,kitchen_info.longitude)
                    com_inst = RiderComissionsettings.objects.first()
                    calc_dist =  float((the_distance * 1000)/com_inst.by_distance) *  float(com_inst.amount_share)
                    print("rider_share_amount int",calc_dist)
                    calc_dist = float(calc_dist)
                    print("rider_share_amount float",calc_dist)
                    print("rider_share_amount after",truncate_float(calc_dist,2))
                    RiderDeliveryPayment.objects.create(
                        rider_id = rider,
                        order_id= order_id,
                        rider_share_amount = truncate_float(calc_dist,2)
                    )
                    RiderOrders.objects.create(rider_id=rider,order_id=order_id,delivery_distance=the_distance)
                    # Orders.objects.filter(pk=order_id).update(status="ready_for_pickup")
                    order_rads.status = "ready_for_pickup"
                    order_rads.rider_pending = False
                    order_rads.save()
                    rider_pk = get_object_or_404(RiderDetails.objects.only('registration_id'), pk=rider) 
                    send_push_message(rider_pk.registration_id, "Ready for Pickup: Your Next Delivery Awaits!", {"link": "/(tabs)/order"})
                    try: 
                        extra = {"newData": "1"}
                        send_salient_data_message(rider_pk.registration_id, extra)
                    except Exception as e:
                        print("Error sending silent message to Rider:", e)
                    data = {'status': 'success', 'message': 'Rider assigned successfully!'}  
                    try:
                        customer_fcm = get_object_or_404(Orders.objects.only('order_fcm'), pk=order_id) 
                        send_push_message(customer_fcm.order_fcm, "Hot and Fresh! Your Order is Ready for Pickup/Delivery.", {"link": "/(tabs)/pastOrders/" + str(order_id)} ) 
                    except:
                        print("order ready for pickup to customer from dashboard rider pending order notif send fail")
                        try:
                            send_order_notification_fcmi({"registration_tokens":[customer_fcm.order_fcm],"id": order_id,"text":"your order number is" + str(order_id),"title": "Hot and Fresh! Your Order is Ready for Pickup/Delivery.",'orders':[order_id],"session_image":"https://relatable-bucket.s3.amazonaws.com/static/session_images/PointingAarowInward.png"})
                        except Exception as ee:
                            print("ready for pickup message from rider pending orders not sent to web customer",ee)            
                # rider_instance = RiderDetails.objects.filter(id=rider_id).first()
                # order_instance = Orders.objects.filter(id=order_id).first()
                
            

                # Send Rider Notification
                # rider_token = rider_instance.registration_id	
                # rider_message = 'Ready for Pickup: Your Next Delivery Awaits!'
                # send_push_message(rider_token, rider_message)
                # print("messaged sent")


                # End Send Rider Notification


                # # Start Push Notification customer app
                # cos_token = order_instance.order_fcm
                # cos_message = 'your rider is on the way!'
                # extra = {"link": "/(tabs)/Orders/singleOrder"}
                # send_push_message(cos_token, cos_message,extra)
                # print("messaged sent")
                # #  End Push Notification customer app

                
            else:
                data = {'status': 'success', 'message': 'Rider already assigned!'}
     
        else:
            data = {'status': 'error', 'message': 'Order or Rider not found'}
        
        return JsonResponse(data)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
def FetchOrderNoteModal(request):

    if request.method == 'POST':
       
        order_id = request.POST.get('order_id')
        print("order_id",order_id)
    

        order_instance = Orders.objects.filter(id= order_id).first()
        

        
        response_data = {
            'status': 'success',
            'notes': order_instance.extra_notes
            

        }

        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def AddOrderNoteModal(request):

    if request.method == 'POST':
       
        order_id = request.POST.get('order_id')
        print("order_id",order_id)
    
        order_notes = request.POST.get('order_notes') or None
        print("order_notes",order_notes)

        
        
        if order_notes:
                order_notes = cleanhtml(order_notes)

        order_instance = Orders.objects.filter(id= order_id).first()
        order_instance.extra_notes = order_notes
        order_instance.save()
        
        response_data = {
            'status': 'success',
            

        }

        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)