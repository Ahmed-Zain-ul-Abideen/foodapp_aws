from django.shortcuts import render,redirect, HttpResponseRedirect
from webApp.models import *
from django.contrib import messages
from django.core.paginator import Paginator
from geopy.geocoders import Nominatim
from django.http import JsonResponse
from django.contrib.auth.models import User,Permission,Group
from django.contrib.auth import logout
from webApp.templatetags.webApp_extras import user_role
from webApp.views.expo_notif_view import send_push_message,send_salient_data_message
from  webApp.views.Others.fcm_notifs  import  *
from datetime import date, timedelta
from django.db.models import Max
import  json

def OrderStatusList(request):  
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    
    if request.user.is_superuser:
    
        all_order_status = Orderstatus.objects.exists()
        if not all_order_status:
            ven = "Not Found"
            
        else: 
            p = Paginator(Orderstatus.objects.all().order_by('-id'),15)
            page = request.GET.get('page')
            ven = p.get_page(page) 
        context = {'ven':ven}
        return render(request, 'dashboard/Order_Status/index.html', context)
    else:
        return render(request, 'dashboard/permission_denied.html')
    


def AddOrderStatusForm(request,add_button_clicked=None):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if request.user.is_superuser:
        re_render = False
        all_role = Group.objects.all()
        role_list = [group.name for group in all_role]

        context= {'re_render':re_render,'all_role':all_role,'role_list':role_list}
        return render(request, 'dashboard/Order_Status/add_order_status_form.html', context)
    else:
        return render(request, 'dashboard/permission_denied.html')
    
def EditOrderStatusForm(request,id,add_button_clicked=None):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if request.user.is_superuser:
        re_render = False
        order_status_instance = Orderstatus.objects.filter(id = id).first()
        all_role = Group.objects.all()
        role_list = [group.name for group in all_role]

        print("check alpha ",order_status_instance.status_title)


        context= {'re_render':re_render,'order_status_instance':order_status_instance,'role_list':role_list,'all_role':all_role}
        return render(request, 'dashboard/Order_Status/edit_order_status_form.html', context)
    else:
        return render(request, 'dashboard/permission_denied.html')



def AddOrderStatus(request):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if request.user.is_superuser:
        if request.method == 'POST':
            
            status_title = request.POST.get('status_title') or None
            print("status_title",status_title)

            if status_title is None:
                user_added_warning = 'Please enter title!'  
                messages.warning(request, user_added_warning)
                return redirect(request.META.get('HTTP_REFERER'))
            

            selected_role = request.POST.getlist('selected_module_dropdown') or None
            print("selected_role",selected_role)

            if selected_role is None:
                user_added_warning = 'Please select role!'  
                messages.warning(request, user_added_warning)
                return redirect(request.META.get('HTTP_REFERER'))
            
            role_instance = Group.objects.filter(id = int(selected_role[0]) ).first()

            order_status_instance = Orderstatus.objects.create(status_title = status_title, role = role_instance.name )
            order_status_instance.save()
            


            group_added_success = 'Status added successfully !'  
            messages.success(request, group_added_success)
            
                
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'dashboard/permission_denied.html')
    




def EditOrderStatus(request):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if request.user.is_superuser: 
        
        order_status_pk = request.POST.get('order_status_pk') or None
        print("order_status_pk",order_status_pk)

        order_status_title = request.POST.get('status_title') or None
        print("order_status_title",order_status_title)



        if order_status_title is None:
            user_added_warning = 'Please enter title!'  
            messages.warning(request, user_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))
        
        # selected_role = request.POST.getlist('selected_module_dropdown') or None
        # print("selected_role",selected_role)

        # if selected_role is None:
        #     user_added_warning = 'Please select role!'  
        #     messages.warning(request, user_added_warning)
        #     return redirect(request.META.get('HTTP_REFERER'))


        status_color = request.POST.get('status_color') or None
        print("status_color",status_color)



        if status_color is None:
            user_added_warning = 'Please select color code!'  
            messages.warning(request, user_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))

        order_status_intance = Orderstatus.objects.filter(pk = order_status_pk).first()
        # role_instance = Group.objects.filter(id = int(selected_role[0]) ).first()

        order_status_intance.status_title = order_status_title
        # order_status_intance.role = role_instance.name
        order_status_intance.its_color_code = status_color
        order_status_intance.save()


        group_added_success = 'Order status updated successfully !'  
        messages.success(request, group_added_success)
            
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'dashboard/permission_denied.html')



from fcm_django.models import FCMDevice



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
            Order_instance.its_color_code = status_instance.its_color_code
            Order_instance.to_be_confirmed = False
            
            # Start Send Push Notification to Register Kitchen Owner on Order Confirmation by Call Agent
            if  status_instance.is_cancelled:
                Order_instance.is_cancelled = True
            else:  
                # send notification
                kitchen_instance = Kitchen.objects.filter(id= Order_instance.kitchen.pk).first()
                print("kitchen instance",kitchen_instance.pk)
                if  FCMDevice.objects.filter(user_id= kitchen_instance.approved_owner.pk).filter(active=True).exists():
                    fcm_device_instance = FCMDevice.objects.filter(user_id= kitchen_instance.approved_owner.pk).filter(active=True)
                    for  device  in fcm_device_instance:
                        token = device.registration_id
                        print("token",token)
                        message = 'Get Ready to Cook! New Order recently assigned to your kitchen'  
                        try:
                            # token = 'ExponentPushToken[TaigETFvKvM4F_0vGKGlD8]'
                            # if Daily Order
                            # if  OrderItems.objects.filter(order_id = Order_instance.pk).exists():
                            #     extra = {"link": "/(tabs)/orders"}
                            # else:
                            #     # if Menu Order 
                            #     extra = {"link": "/(tabs)/orders"}
                            extra = {"link": "/(tabs)/orders"}
                            send_push_message(token, message, extra)
                            print("messaged sent")
                        except:
                            print("messaged not  sent to kitchen app device",device.registration_id)
                            try:
                                send_kitchen_notification_fcmi({"registration_tokens":[token],"id": order_id,"text":"the order number is" + str(order_id),"title":  message,'orders':[order_id],"session_image":"https://relatable-bucket.s3.amazonaws.com/static/session_images/PointingAarowInward.png"})
                            except Exception as ee:
                                print("ready to cook message not sent to kitchen web",ee)


                        try: 
                            extra = {"newData": "1"}
                            send_salient_data_message(device.registration_id, extra)
                        except Exception as e:
                            print("Error sending silent message to kitchen get ready cook:", e)

                else:
                    print("messaged not  sent no active device for kitchen")

            if  status_instance.is_cancelled:
                Order_instance.save()
            else:
                if    Order_instance.has_menu:
                    print("order has menu")
                    order_menus_max = MenuCategory.objects.filter(pk__in= list(Menu.objects.filter(pk__in= list(OrderMenuItems.objects.filter(order_id=Order_instance.pk).values_list('menu_id',flat=True))).values_list('category_id',flat=True))).aggregate(Max('menu_count'))
                    print("['menu_count__max']",order_menus_max)
                    order_menus_max =  order_menus_max.get('menu_count__max')
                    Order_instance.max_deliverable = order_menus_max
                    days_limit = order_menus_max  -  1
                    Order_instance.last_date_to_deliver =  date.today() + timedelta(days=days_limit)
                    print("has menu above completed") 
                else:
                    Order_instance.last_date_to_deliver  =  date.today()
                Order_instance.save()

                if   Order_instance.has_menu:
                    menus_ordered  = OrderMenuItems.objects.filter(order_id=Order_instance.pk)
                    for  menu_order  in  menus_ordered:
                        menu_inst = Menu.objects.filter(pk=menu_order.menu_id).first()
                        the_items = json.decoder.JSONDecoder().decode(menu_inst.associated_items)
                        print("till json decode")
                        the_items_list = list(the_items.values())
                        print("dict values list",the_items_list)
                        the_items_list_int = [eval(i) for i in the_items_list] 
                        print("dict values list",the_items_list)
                        menu_cat = MenuCategory.objects.filter(pk=menu_inst.category_id).first()
                        for  i  in range(0,menu_cat.menu_count):
                            MenuFoodRecords.objects.create(
                                order_id =  Order_instance.pk,
                                menu_id =  menu_inst.pk,
                                item_id =  the_items_list_int[i],
                                quantity =  menu_order.quantity,
                                delivery_date =  date.today()  +  timedelta(days=i)
                            )

                if   OrderItems.objects.filter(order_id=Order_instance.pk).exists():
                    OrderItems.objects.filter(order_id=Order_instance.pk).update(delivery_date=date.today())

                if   OrderDealItems.objects.filter(order_id=Order_instance.pk).exists():
                    OrderDealItems.objects.filter(order_id=Order_instance.pk).update(delivery_date=date.today())

            # else:
            #     print("inelse")
            #     pass

            # End Send Push Notification to Register Kitchen Owner on Order Confirmation by Call Agent

            # Start Push Notification customer app
            

            cos_token = Order_instance.order_fcm
            # cos_token = 'ExponentPushToken[CmDGosEnqa3AZbocygQ_vy]'
            
            if status_instance.is_cancelled:
                cos_message = 'Your order is canceled!'
            else:
                cos_message = 'Your order is confirmed! We are on it and processing it now.'

            try:
                extra = {"link": "/(tabs)/pastOrders/" + str(order_id)}
                send_push_message(cos_token, cos_message,extra)
                print("messaged sent to customer")
            except Exception as e:
                print("message not sent to app customer",e)
                try:
                    send_order_notification_fcmi({"registration_tokens":[cos_token],"id":Order_instance.pk,"text":"your order number is" + str(Order_instance.pk),"title":cos_message,'orders':[Order_instance.pk],"session_image":"https://relatable-bucket.s3.amazonaws.com/static/session_images/PointingAarowInward.png"})
                except Exception as ee:
                    print("message not sent to web customer",ee)

            try: 
                extra = {"newData": "4"}
                send_salient_data_message(Order_instance.order_fcm, extra)
            except Exception as e:
                print("Error sending silent message to customer order confirmed:", e)

            

            #  End Push Notification customer app
            data = {'status': 'success', 'message': 'Status updated successfully!','last_one':last_one}
        else:
            data = {'status': 'error', 'message': 'Order or Status not found'}
        
        return JsonResponse(data)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


# from Search table status change:
def EditOrderStatusNotifSearch(request):

    if request.method == 'POST':
        print('here in search order satatus change')
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
            Order_instance.its_color_code = status_instance.its_color_code
            Order_instance.to_be_confirmed = False
            
            # Start Send Push Notification to Register Kitchen Owner on Order Confirmation by Call Agent
            if  status_instance.is_cancelled:
                Order_instance.is_cancelled = True
            else:  
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
                            # if  OrderItems.objects.filter(order_id = Order_instance.pk).exists():
                            #     extra = {"link": "/(tabs)/daily_orders"}
                            # else:
                                # if Menu Order 
                            extra = {"link": "/(tabs)/other_orders"}
                            send_push_message(token, message, extra)
                            print("messaged sent")
                        except:
                            print("messaged not  sent to device",device.registration_id)

                        try: 
                            extra = {"newData": "1"}
                            send_salient_data_message(device.registration_id, extra)
                        except Exception as e:
                            print("Error sending silent message to kitchen get ready cook:", e)

                else:
                    print("messaged not  sent no active device for kitchen")

            
            if    Order_instance.has_menu:
                print("order has menu")
                order_menus_max = MenuCategory.objects.filter(pk__in= list(Menu.objects.filter(pk__in= list(OrderMenuItems.objects.filter(order_id=Order_instance.pk).values_list('menu_id',flat=True))).values_list('category_id',flat=True))).aggregate(Max('menu_count'))
                print("['menu_count__max']",order_menus_max)
                order_menus_max =  order_menus_max.get('menu_count__max')
                Order_instance.max_deliverable = order_menus_max
                days_limit = order_menus_max  -  1
                Order_instance.last_date_to_deliver =  date.today() + timedelta(days=days_limit)
                print("has menu above completed") 
            else:
                Order_instance.last_date_to_deliver  =  date.today()
            Order_instance.save()

            if   Order_instance.has_menu:
                menus_ordered  = OrderMenuItems.objects.filter(order_id=Order_instance.pk)
                for  menu_order  in  menus_ordered:
                    menu_inst = Menu.objects.filter(pk=menu_order.menu_id).first()
                    the_items = json.decoder.JSONDecoder().decode(menu_inst.associated_items)
                    print("till json decode")
                    the_items_list = list(the_items.values())
                    print("dict values list",the_items_list)
                    the_items_list_int = [eval(i) for i in the_items_list] 
                    print("dict values list",the_items_list)
                    menu_cat = MenuCategory.objects.filter(pk=menu_inst.category_id).first()
                    for  i  in range(0,menu_cat.menu_count):
                        MenuFoodRecords.objects.create(
                            order_id =  Order_instance.pk,
                            menu_id =  menu_inst.pk,
                            item_id =  the_items_list_int[i],
                            quantity =  menu_order.quantity,
                            delivery_date =  date.today()  +  timedelta(days=i)
                        )

            if   OrderItems.objects.filter(order_id=Order_instance.pk).exists():
                OrderItems.objects.filter(order_id=Order_instance.pk).update(delivery_date=date.today())

            # else:
            #     print("inelse")
            #     pass

            # End Send Push Notification to Register Kitchen Owner on Order Confirmation by Call Agent

            # Start Push Notification customer app
            

            cos_token = Order_instance.order_fcm
            # cos_token = 'ExponentPushToken[CmDGosEnqa3AZbocygQ_vy]'
            
            if status_instance.is_cancelled:
                cos_message = 'Your order is canceled!'
            else:
                cos_message = 'Your order is confirmed! We are on it and processing it now.'

            try:
                extra = {"link": "/(tabs)/pastOrders/" + str(order_id)}
                send_push_message(cos_token, cos_message,extra)
                print("messaged sent to customer")
            except:
                print("message not sent to app customer")
                try:
                    send_order_notification_fcmi({"registration_tokens":[cos_token],"id":Order_instance.pk,"text":"your order number is" + str(Order_instance.pk),"title":cos_message,'orders':[Order_instance.pk],"session_image":"https://relatable-bucket.s3.amazonaws.com/static/session_images/PointingAarowInward.png"})
                except Exception as ee:
                    print("message not sent to web customer",ee)


            try: 
                extra = {"newData": "4"}
                send_salient_data_message(Order_instance.order_fcm, extra)
            except Exception as e:
                print("Error sending silent message to customer order confirmed:", e)

            

            #  End Push Notification customer app
            data = {'status': 'success', 'message': 'Status updated successfully!','last_one':last_one}
        else:
            data = {'status': 'error', 'message': 'Order or Status not found'}
        
        return JsonResponse(data)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})




def DeleteOrderStatus(request):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    
    if request.user.is_superuser:
    
        print("here for deleteing order status record")
        order_status_id = request.GET.get("order_status_id")    
        print("order_status_id", order_status_id)
        order_status_instance = Orderstatus.objects.filter(id=order_status_id).first()
        order_status = order_status_instance.status_title

        order_status_instance.delete() 
        print("record deleted Successfully!")
        data = {'role_name':order_status}
        return JsonResponse(data)
    else:
        return render(request, 'dashboard/permission_denied.html')