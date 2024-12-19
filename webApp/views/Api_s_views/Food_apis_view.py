from rest_framework.views import APIView
from rest_framework import status
from webApp.views.Others.geocode_address import *
from django.contrib.auth.models import User
from webApp.models import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  
from webApp.Serializers.Food_api_serializer import *
from webApp.Serializers.kitchen_api_serializer import *
from fcm_django.models import FCMDevice
from webApp.Serializers.kitchen_api_serializer  import *
from django.db.models import Count
from collections import Counter
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
channel_layer = get_channel_layer()
from  webApp.utils  import  truncate_float
from  webApp.views.expo_notif_view import send_push_message,send_salient_data_message
from  webApp.views.Others.fcm_notifs  import  *
from django.shortcuts import get_object_or_404
from  webApp.Serializers.User_api_serializer  import  MyallordersSerializer
from datetime import date, timedelta

#Get All Menus 
class GetAllMenus(APIView):
    def  get(self,request):
        if  MenuCategory.objects.exclude(menu_count=1).exists():
            serialized_data = MenuCategorysSerializer(MenuCategory.objects.annotate(menus_count=Count('menu_categories')).exclude(menus_count=0).exclude(menu_count=1).all(),many=True)
            return Response(serialized_data.data,status=status.HTTP_200_OK)
        else:
            return Response(data={'message':"Other Menus didnot found"},status=status.HTTP_404_NOT_FOUND)

#Get Daily Food Items 
class GetDailyFoodItems(APIView):
    def  get(self,request):
        if Menuitems.objects.filter(daily_deals=True).exists():
            serialized_data = DailyMenuitemsSerializer(Menuitems.objects.filter(daily_deals=True),many=True)
            return Response(serialized_data.data,status=status.HTTP_200_OK)
        else:
            return Response(data={'message':"No items found"},status=status.HTTP_404_NOT_FOUND)
        
#Get Adds on Items 
class GetAddsonItems(APIView):
    def  get(self,request):
        if Menuitems.objects.filter(ads_on=True).exists():
            serialized_data = DailyMenuitemsSerializer(Menuitems.objects.filter(ads_on=True),many=True)
            return Response(serialized_data.data,status=status.HTTP_200_OK)
        else:
            return Response(data={'message':"No items found"},status=status.HTTP_404_NOT_FOUND)
        

#Get my Orders 
class  GetmyOrders(APIView):
    def  get(self,request,my_email):
        if   Orders.objects.annotate(menu_orders_count=Count('order_menu_items')).filter(menu_orders_count=0).filter(user=my_email).exists():
            serialized_data = KitchenOrdersSerializer(Orders.objects.annotate(menu_orders_count=Count('order_menu_items')).filter(menu_orders_count=0).filter(user=my_email),many=True)
            return Response(serialized_data.data,status=status.HTTP_200_OK)
        else:
            return Response(data={'message':"No orders found for this user"},status=status.HTTP_404_NOT_FOUND)
        

#Get my menu Orders 
class  GetmyMenuOrders(APIView):
    def  get(self,request,my_email):
        if   Orders.objects.annotate(menu_orders_count=Count('order_menu_items')).exclude(menu_orders_count=0).filter(user=my_email).exists():
            serialized_data = MenuOrdersSerializer(Orders.objects.annotate(menu_orders_count=Count('order_menu_items')).exclude(menu_orders_count=0).filter(user=my_email),many=True)
            return Response(serialized_data.data,status=status.HTTP_200_OK)
        else:
            return Response(data={'message':"No menu orders found for this user"},status=status.HTTP_404_NOT_FOUND)

#Save Food order 
class  SaveFoodOrder(APIView):
    def  post(self, request): 

        customer_address = request.data.get('customer_address')
        print("customer_address",customer_address)
        if customer_address is None:
            data = {'message': 'Please Enter customer address'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        lat = None

        try:
            lat, long = OpenCage_for_address(customer_address)
            print("order api  lat long",lat,long)
        except:
            data = {'message': 'This address cannot be located please enter valid one'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        if lat is None:
            data = {'message': 'This address cannot be traced please enter valid one'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

        item_id = request.data.get('item_id') or None
        if item_id is None:
            data = {'message': 'Please Enter item  id'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

        
        contact = request.data.get('contact')
        print("contact",contact)
        if contact is None:
            data = {'message': 'Please Enter  contact number'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

        quantity = request.data.get('quantity')
        if quantity is None:
            data = {'message': 'Please Enter  quantity'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

        is_cod = request.data.get('is_cod')
        print("is_cod",is_cod)
        if is_cod is None:
            data = {'message': 'Please Enter  is_cod'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

        
        subscription_info = request.data.get('subscription_info') or None
        print("subscription_info",subscription_info)
        
        

        if  not  Menuitems.objects.filter(pk=item_id).exists():
            data = {'message': 'Please Enter valid item  id'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        
        # try:
        order_kitchen,the_distance = lat_long_nearest_kitchen(lat,long)

        if  order_kitchen  ==  3276:
            data = {'message': 'Sorry we are not operating in your area'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        elif  order_kitchen  is None:
            data = {'message': 'Sorry there is no kitchen at the moment to serve your order'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        # except:
        #     order_kitchen = None 
        
        
        item_price = request.data.get('item_price') or None
        if item_price is None:
            data = {'message': 'Please Enter item  price'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

        customer_name = request.data.get('customer_name') or None
        if customer_name is None:
            data = {'message': 'Please Enter customer name'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

        customer_email = request.data.get('customer_email') or None
        if customer_email is None:
            data = {'message': 'Please Enter customer  email'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST) 
        

        order_details = request.data.get('order_details')  
        print("order_details",order_details)
        if order_details is None:
            data = {'message': 'Please Enter order details'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

        selected_addon_ids = request.data.get('selected_addon') or None
        print("selected_addon_ids",selected_addon_ids)
        if selected_addon_ids is None:
            pass
        else:
            if  not len(selected_addon_ids):
                data = {'message': 'Add on cannot be empty'}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            

        total_price = request.data.get('total_price') or None
        if total_price is None:
            data = {'message': 'Please Enter total price'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

        order_fcm = request.data.get('order_fcm') 
        if order_fcm is None:
            data = {'message': 'Please Enter Fcm token'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        
        print("order_fcm",order_fcm)
        if  not   FCMDevice.objects.filter(registration_id=order_fcm).exists(): 
            fcm = FCMDevice(
                registration_id=order_fcm 
            )
            fcm.save() 

        order_instance = Orders.objects.create(user = customer_email,subscription_info=subscription_info,contact=contact,is_cod=is_cod,address_details=customer_address,latitude=lat,longitude=long, customer_name=customer_name,order_fcm=order_fcm, total_price=total_price,kitchen_id=order_kitchen)

        order_instance.save()  

        orderitem_instance = OrderItems.objects.create(order_id = order_instance.pk, item_id = item_id, extra_details= order_details, sub_total= item_price,quantity=quantity)

        orderitem_instance.save()

        if selected_addon_ids is None:
            pass
        else:
            if   any(isinstance(item, dict) for item in selected_addon_ids):
                for   item  in selected_addon_ids:
                    OrderAddson.objects.create(order_id = order_instance.pk, item_id = item.get('id'), quantity =item.get('quantity'))

            else:

                # Original list of integers
                integer_list =  selected_addon_ids

                # Count the occurrences of each integer in the list
                counts = Counter(integer_list)

                # Create a list of tuples where each tuple is (integer, count)
                result = [(num, count) for num, count in counts.items()]

                print(result)
                for item in result: 
                    # print("id",item,type(item))
                    # count = selected_addon_ids.count(str(item))
                    # print("count",count)
                    OrderAddson.objects.create(order_id = order_instance.pk, item_id = item[0], quantity =item[1])

        #Payment for kitchen 
        if     MenuCategory.objects.filter(menu_count=1).exclude(Kitchen_share_percent=None).exists():
            payment_percentage  =  MenuCategory.objects.filter(menu_count=1).first() 
            try:
                kitchen_share_amount = float(payment_percentage.Kitchen_share_percent)/float(100)   *  float(total_price)
                print("kitchen_share_amount",kitchen_share_amount)
                print("kitchen_share_amount",truncate_float(kitchen_share_amount,2))
            
                kitchenOrdersPayment.objects.create(
                    Kitchen_id = order_kitchen, 
                    order_id =  order_instance.pk,
                    kitchen_share_amount =   truncate_float(kitchen_share_amount,2)
                )
            except:
                kitchen_share_amount = 10/100   *  total_price
                print("into percentage exception")
                print("kitchen_share_amount",kitchen_share_amount)
                print("kitchen_share_amount",truncate_float(kitchen_share_amount,2))
                kitchenOrdersPayment.objects.create(
                    Kitchen_id = order_kitchen, 
                    order_id =  order_instance.pk,
                    kitchen_share_amount =   truncate_float(kitchen_share_amount,2)
                )
        else:
            kitchen_share_amount = 10/100   *  total_price
            print("into percentage  else")
            print("kitchen_share_amount",kitchen_share_amount)
            print("kitchen_share_amount",truncate_float(kitchen_share_amount,2))
            kitchenOrdersPayment.objects.create(
                Kitchen_id = order_kitchen, 
                order_id =  order_instance.pk,
                kitchen_share_amount =   truncate_float(kitchen_share_amount,2)
            )

            


        try:
            #Send WebSocket notification
            async_to_sync(channel_layer.group_send)(
                'orders_listing_group',
                {
                    'type': 'send_order_list_notification',
                    'message': f'Order {order_instance.pk} has been submitted!'
                }
            )
            print("webscoket  have updated agent orders list")
        except:
            print("webscoket  amybe closed")
        data = {'message': 'Order submitted successfully','order_id':order_instance.pk,'total_price':total_price}
        return Response(data, status=status.HTTP_200_OK)



#Save order status 
class  SaveOrderStatus(APIView):
    permission_classes = (IsAuthenticated,)
    def  post(self, request):  

        order_id = request.data.get('order_id') or None
        print("order_id ",order_id)
        if order_id is None:
            data = {'message': 'Please Enter order id'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        if  not  Orders.objects.filter(pk=order_id).exists():
            data = {'message': 'Please Enter valid order id'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

        # has_menu = request.data.get('has_menu')
        # print("has_menu ",has_menu)
        # if has_menu is None:
        #     # has_menu = False
        #     data = {'message': 'Please Enter has_menu is True or False'}
        #     return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        order_status = request.data.get('order_status') or None
        if order_status is None:
            data = {'message': 'Please Enter order status'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        order_status_id = request.data.get('order_status_id') or None
        if order_status_id is None:
            data = {'message': 'Please Enter order status  id'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        
        is_pickup = request.data.get('is_pickup')
        if  is_pickup is None:
            data = {'message': 'Please Enter  is  pickup  bit is True or False'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        print("is_pickup",is_pickup)

        is_in_process = request.data.get('is_in_process')
        if  is_in_process is None:
            data = {'message': 'Please Enter  is  in process  bit is True or False'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        print("is_in_process",is_in_process)

        if   OrderProcessedStatuses.objects.filter(processed_date=date.today()).filter(order_id=order_id).filter(status_id=order_status_id).exists():
            data = {'message': 'This status is already processed today for this order !'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        rider_p= False
        this_order = Orders.objects.filter(pk=order_id).first()
        if   is_pickup:
            # try:
                kitchen_info = KitchenAddress.objects.filter(Kitchen_id=this_order.kitchen_id).first()
                 
                rider, the_distance = lat_long_nearest_rider(kitchen_info.latitude,kitchen_info.longitude)
                print("rider for notif",rider," distance",the_distance)
                if  rider  is  None:
                    #Orders.objects.filter(pk=order_id).update(rider_pending=True)
                    this_order.rider_pending = True
                    rider_p= True
                    # data = {'message': 'Please try again later because no rider found at the moment'}
                    # return Response(data, status=status.HTTP_409_CONFLICT)
                else:
                    #order_rads = Orders.objects.filter(pk=order_id).first()
                    the_distance  =  float(the_distance)  +  float(this_order.kitchen_to_customer_distance)
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
                    rider_pk = get_object_or_404(RiderDetails.objects.only('registration_id'), pk=rider) 
                    send_push_message(rider_pk.registration_id, "Ready for Pickup: Your Next Delivery Awaits!", {"link": "/(tabs)/order"})
                    try: 
                        extra = {"newData": "1"}
                        send_salient_data_message(rider_pk.registration_id, extra)
                    except Exception as e:
                        print("Error sending silent message to Rider:", e)

                    try:
                        #customer_fcm = get_object_or_404(Orders.objects.only('order_fcm'), pk=order_id) 
                        send_push_message(this_order.order_fcm, "Hot and Fresh! Your Order is Ready for Pickup/Delivery.", {"link": "/(tabs)/pastOrders/" + str(order_id)} ) 
                    except:
                        print("order ready for pickup to customer  notif send fail") 
                        try:
                            send_order_notification_fcmi({"registration_tokens":[this_order.order_fcm],"id": order_id,"text":"your order number is" + str(order_id),"title": "Hot and Fresh! Your Order is Ready for Pickup/Delivery.",'orders':[order_id],"session_image":"https://relatable-bucket.s3.amazonaws.com/static/session_images/PointingAarowInward.png"})
                        except Exception as ee:
                            print("ready for pickup message not sent to web customer",ee)

                # if  has_menu:
                tomorrow = date.today() + timedelta(days=1)
                #Orders.objects.filter(pk=order_id).update(kitchen_pickup_date=tomorrow)
                this_order.kitchen_pickup_date = tomorrow
            # except:
            #     data = {'message': 'Something went wrong while getting rider'}
            #     return Response(data, status=status.HTTP_400_BAD_REQUEST)
                status_code = Orderstatus.objects.filter(is_pickup=True).first()
                #Orders.objects.filter(pk=order_id).update(its_color_code=status_code.its_color_code)
                this_order.its_color_code = status_code.its_color_code
                if  OrderItems.objects.filter(order_id=order_id).filter(delivery_date=date.today()).exists():
                    OrderItems.objects.filter(order_id=order_id).filter(delivery_date=date.today()).update(is_cooked=True)

                if  OrderDealItems.objects.filter(order_id=order_id).filter(delivery_date=date.today()).exists():
                    OrderDealItems.objects.filter(order_id=order_id).filter(delivery_date=date.today()).update(is_cooked=True)

                if  MenuFoodRecords.objects.filter(order_id=order_id).filter(delivery_date=date.today()).exists():
                    MenuFoodRecords.objects.filter(order_id=order_id).filter(delivery_date=date.today()).update(is_cooked=True)

                kitchenOrdersPayment.objects.filter(order_id=order_id).update(is_payable=True)

                # if  this_order.last_date_to_deliver == date.today():
                #     #Kitchen payments 
                #     try:
                #         kitchen_perc = FoodappSettings.objects.last()
                #         kitchen_share_amount = float(kitchen_perc.Kitchen_share_percent)/float(100)   *  float(this_order.total_price)
                #         print("kitchen_share_amount",kitchen_share_amount)
                #         print("kitchen_share_amount",truncate_float(kitchen_share_amount,2))
                    
                #         kitchenOrdersPayment.objects.create(
                #             Kitchen_id = this_order.kitchen_id, 
                #             order_id =  order_id,
                #             kitchen_share_amount =   truncate_float(kitchen_share_amount,2)
                #         )
                #     except:
                #         kitchen_share_amount = float(10/100)   * float(this_order.total_price)
                #         print("into percentage exception")
                #         print("kitchen_share_amount",kitchen_share_amount)
                #         print("kitchen_share_amount",truncate_float(kitchen_share_amount,2))
                #         kitchenOrdersPayment.objects.create(
                #             Kitchen_id = this_order.kitchen_id, 
                #             order_id =  order_id,
                #             kitchen_share_amount =   truncate_float(kitchen_share_amount,2)
                #         )
        
        
        if   is_in_process:
            status_code = Orderstatus.objects.filter(is_in_process=True).first()
            #Orders.objects.filter(pk=order_id).update(its_color_code=status_code.its_color_code)
            this_order.its_color_code = status_code.its_color_code
            try:
                #customer_fcm = get_object_or_404(Orders.objects.only('order_fcm'), pk=order_id) 
                send_push_message(this_order.order_fcm, "On the Heat: Your Delicious Order is in the Works!", {"link": "/(tabs)/pastOrders/" + str(order_id)} ) 
            except:
                print("order in process notif send fail to app")
                try:
                    send_order_notification_fcmi({"registration_tokens":[this_order.order_fcm],"id": order_id,"text":"your order number is" + str(order_id),"title": "On the Heat: Your Delicious Order is in the Works!",'orders':[order_id],"session_image":"https://relatable-bucket.s3.amazonaws.com/static/session_images/PointingAarowInward.png"})
                except Exception as ee:
                    print("in process message not sent to web customer",ee)
        
        if  rider_p:
            order_status = order_status  + " (rider pending)"
            #Orders.objects.filter(pk=order_id).update(status=order_status)
            this_order.status = order_status
        else:
            #Orders.objects.filter(pk=order_id).update(status=order_status)
            this_order.status = order_status
     
        OrderProcessedStatuses.objects.create(order_id=order_id,status_id=order_status_id)
        this_order.save()

        try: 
            extra = {"newData": "4"}
            send_salient_data_message(this_order.order_fcm, extra)
        except Exception as e:
            print("when kitchen changes orders status   Error sending silent message to customer:", e)
 

        data = {'message': 'Order status updated successfuly'}
        return Response(data, status=status.HTTP_200_OK)



#Save Menu order 
class  SaveMenuOrder(APIView):
    def  post(self, request): 

        customer_address = request.data.get('customer_address') or None
        if customer_address is None:
            data = {'message': 'Please Enter customer address'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        lat = None

        try:
            lat, long = OpenCage_for_address(customer_address)
            print("order api  lat long",lat,long)
        except:
            data = {'message': 'This address cannot be located please enter valid one'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        if lat is None:
            data = {'message': 'This address cannot be traced please enter valid one'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        contact = request.data.get('contact')
        if contact is None:
            data = {'message': 'Please Enter  contact number'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

        quantity = request.data.get('quantity')
        if quantity is None:
            data = {'message': 'Please Enter  quantity'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

        is_cod = request.data.get('is_cod')
        if is_cod is None:
            data = {'message': 'Please Enter  is_cod'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

        menu_id = request.data.get('menu_id') or None
        if menu_id is None:
            data = {'message': 'Please Enter menu  id'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

        if  not  Menu.objects.filter(pk=menu_id).exists():
            data = {'message': 'Please Enter valid menu  id'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        
        order_kitchen,the_distance = lat_long_nearest_kitchen(lat,long)

        if  order_kitchen  ==  3276:
            data = {'message': 'Sorry we are not operating in your area'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        elif  order_kitchen  is None:
            data = {'message': 'Sorry there is no kitchen at the moment to serve your order'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    
        
        
        menu_price = request.data.get('menu_price') or None
        if menu_price is None:
            data = {'message': 'Please Enter menu  price'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        
        customer_name = request.data.get('customer_name') or None
        if customer_name is None:
            data = {'message': 'Please Enter customer name'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

        customer_email = request.data.get('customer_email') or None
        if customer_email is None:
            data = {'message': 'Please Enter customer  email'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST) 
        

           

        order_fcm = request.data.get('order_fcm') 
        print("menu order fcm",order_fcm)
        if order_fcm is None:
            data = {'message': 'Please Enter Fcm token'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        if  not   FCMDevice.objects.filter(registration_id=order_fcm).exists(): 
            fcm = FCMDevice(
                registration_id=order_fcm 
            )
            fcm.save() 

        updated_total = float(menu_price) * float(quantity)
        order_instance = Orders.objects.create(user = customer_email,is_cod=is_cod,contact=contact,address_details=customer_address,latitude=lat,longitude=long, customer_name=customer_name,order_fcm=order_fcm, total_price= updated_total,kitchen_id=order_kitchen)

        order_instance.save()  

        ordermenu_instance = OrderMenuItems.objects.create(order_id = order_instance.pk, menu_id = menu_id,  sub_total= menu_price,quantity=quantity)

        ordermenu_instance.save() 


        #Payment for kitchen 
        menu_instance =  Menu.objects.filter(pk=menu_id).first()
        if  menu_instance.total_price is None:
            total_price = 185.58
        else:
            total_price = menu_instance.total_price
            total_price = float(total_price) * float(quantity)
        if     MenuCategory.objects.filter(pk=menu_instance.category_id).exclude(Kitchen_share_percent=None).exists():
            payment_percentage  =  MenuCategory.objects.filter(pk=menu_instance.category_id).first() 
            try:
                kitchen_share_amount = float(payment_percentage.Kitchen_share_percent)/float(100)   *  total_price
                print("kitchen_share_amount",kitchen_share_amount)
                print("kitchen_share_amount",truncate_float(kitchen_share_amount,2))
            
                kitchenOrdersPayment.objects.create(
                    Kitchen_id = order_kitchen, 
                    order_id =  order_instance.pk,
                    kitchen_share_amount =   truncate_float(kitchen_share_amount,2)
                )
            except:
                kitchen_share_amount =  float(10/100)   *  float(total_price)
                print("into percentage exception")
                kitchenOrdersPayment.objects.create(
                    Kitchen_id = order_kitchen, 
                    order_id =  order_instance.pk,
                    kitchen_share_amount =   truncate_float(kitchen_share_amount,2)
                )
        else:
            kitchen_share_amount = float(10/100)   *  float(total_price)
            print("into percentage  else")
            print("kitchen_share_amount",kitchen_share_amount)
            print("kitchen_share_amount",truncate_float(kitchen_share_amount,2))
            kitchenOrdersPayment.objects.create(
                Kitchen_id = order_kitchen, 
                order_id =  order_instance.pk,
                kitchen_share_amount =   truncate_float(kitchen_share_amount,2)
            )

        try:
            #Send WebSocket notification
            async_to_sync(channel_layer.group_send)(
                'orders_listing_group',
                {
                    'type': 'send_order_list_notification',
                    'message': f'Order {order_instance.pk} has been submitted!'
                }
            )
            print("Menu orde webscoket  have updated agent orders list")
        except:
            print("Menu order webscoket  amybe closed")
        data = {'message': 'Order submitted successfully'}
        return Response(data, status=status.HTTP_200_OK)



#Get Single Food Item
class GetSingleFoodItems(APIView):
    def  get(self,request,id):
        if Menuitems.objects.filter(id=id).exists():
            serialized_data = DailyMenuitemsSerializer(Menuitems.objects.filter(id=id))
            return Response(serialized_data.data,status=status.HTTP_200_OK)
        else:
            return Response(data={'message':"No item found"},status=status.HTTP_404_NOT_FOUND)
        

#Get single Order 
class  GetSingleOrder(APIView):
    def  get(self,request,order_id):
        if   Orders.objects.filter(pk=order_id).exists(): 
            return   Response(MyallordersSerializer(Orders.objects.filter(pk=order_id).first()).data,status=status.HTTP_200_OK) 
        else:
            return Response(data={'message':"Please Enter valid order id"},status=status.HTTP_400_BAD_REQUEST)
        


#Get Single Menu 
class GetMenuFood(APIView):
    def  get(self,request,id):
        if Menu.objects.filter(id=id).exists(): 
            return Response(MenuSerializer(Menu.objects.filter(id=id).first()).data,status=status.HTTP_200_OK)
        else:
            return Response(data={'message':"No item found"},status=status.HTTP_404_NOT_FOUND)
        


#Rider order status 
class   RiderUpdateOrderStatus(APIView): 
    def  post(self, request):  

        order_id = request.data.get('order_id') or None
        if order_id is None:
            data = {'message': 'Please Enter order id'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        if  not  Orders.objects.filter(pk=order_id).exists():
            data = {'message': 'Please Enter valid order id'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

        has_menu = request.data.get('has_menu')
        print("has_menu ",has_menu)
        if has_menu is None:
            # has_menu = False
            data = {'message': 'Please Enter has_menu is True or False'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        order_status = request.data.get('order_status') or None
        if order_status is None:
            data = {'message': 'Please Enter order status'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        order_status_id = request.data.get('order_status_id') or None
        if order_status_id is None:
            data = {'message': 'Please Enter order status  id'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        is_delivered = request.data.get('is_delivered')  
        if is_delivered is None:
            data = {'message': 'Please Enter is delivered bit is True or False'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

        is_rider_on_way = request.data.get('is_rider_on_way')  
        if is_rider_on_way is None:
            data = {'message': 'Please Enter is rider on way bit is True or False'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        order_instance = Orders.objects.filter(pk=order_id).first()
        
        if   is_delivered:
            try:
                #customer_fcm = get_object_or_404(Orders.objects.only('order_fcm'), pk=order_id) 
                send_push_message(order_instance.order_fcm, "Your Delicious Order Has Landed!", {"link": "/(tabs)/pastOrders/"   + str(order_id)}) 
            except:
                print("order landed notif send fail to app")
                try:
                    send_order_notification_fcmi({"registration_tokens":[order_instance.order_fcm],"id": order_id,"text":"your order number is" + str(order_id),"title": "Your Delicious Order Has Landed!",'orders':[order_id],"session_image":"https://relatable-bucket.s3.amazonaws.com/static/session_images/PointingAarowInward.png"})
                except Exception as ee:
                    print("order landed message not sent to web customer",ee)
        
        
        
        if   is_rider_on_way:
            status_code = Orderstatus.objects.filter(is_rider_on_way=True).first()
            #Orders.objects.filter(pk=order_id).update(its_color_code=status_code.its_color_code)
            order_instance.its_color_code = status_code.its_color_code
            try:
                #customer_fcm = get_object_or_404(Orders.objects.only('order_fcm'), pk=order_id) 
                send_push_message(order_instance.order_fcm, "Rider Has Picked Up Your Order!", {"link": "/(tabs)/pastOrders/"  + str(order_id)}) 
            except:
                print("order picked up notif send fail to app")
                try:
                    send_order_notification_fcmi({"registration_tokens":[order_instance.order_fcm],"id": order_id,"text":"your order number is" + str(order_id),"title": "Rider Has Picked Up Your Order!",'orders':[order_id],"session_image":"https://relatable-bucket.s3.amazonaws.com/static/session_images/PointingAarowInward.png"})
                except Exception as ee:
                    print("order picked up message not sent to web customer",ee)

        today_Date = date.today()
        rider_latest_order = RiderOrders.objects.filter(order_id=order_id).filter(delivery_date=today_Date).last()
        rider_latest_order.is_delivered = is_delivered
        rider_latest_order.save()
        if  is_delivered:
            RiderDeliveryPayment.objects.filter(order_id=order_id).filter(delivery_date=today_Date).update(is_payable=True)
        if  has_menu:
            if  is_delivered:
                status_code = Orderstatus.objects.filter(is_delivered=True).first() 
                if  order_instance.max_deliverable == 1:
                    order_instance.status = order_status
                    order_instance.is_delivered = True
                elif  order_instance.last_date_to_deliver  and  order_instance.last_date_to_deliver  == date.today():
                    order_instance.status = order_status
                    order_instance.is_delivered = True
                else:
                    order_instance.status = "Partial delivered"
                 
                order_instance.max_deliverable = order_instance.max_deliverable - 1
                order_instance.its_color_code = status_code.its_color_code
                # order_instance.save() 
        else:
            if  is_delivered:
                status_code = Orderstatus.objects.filter(is_delivered=True).first()  
                #Orders.objects.filter(pk=order_id).update(status=order_status,is_delivered=True,max_deliverable=0,its_color_code=status_code.its_color_code)
                order_instance.status = order_status
                order_instance.is_delivered  = True
                order_instance.max_deliverable = 0
                order_instance.its_color_code = status_code.its_color_code
            else:
                #Orders.objects.filter(pk=order_id).update(status=order_status)
                order_instance.status = order_status 

        OrderProcessedStatuses.objects.create(order_id=order_id,status_id=order_status_id)
        order_instance.save()
        try: 
            extra = {"newData": "4"}
            send_salient_data_message(order_instance.order_fcm, extra)
        except Exception as e:
            print("When Rider changes orders status   Error sending silent message to customer:", e)
        data = {'message': 'Order status updated successfuly'}
        return Response(data, status=status.HTTP_200_OK)
    





#Cart Orders
class   CartOrder(APIView):
    def  post(self, request):  

        customer_address = request.data.get('customer_address')
        print("customer_address",customer_address)
        if customer_address is None:
            data = {'message': 'Please Enter customer address'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

        
        lat = None

        try:
            lat, long = OpenCage_for_address(customer_address)
            print("order api  lat long",lat,long)
        except:
            data = {'message': 'This address cannot be located please enter valid one'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        if lat is None:
            data = {'message': 'This address cannot be traced please enter valid one'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        order_kitchen,the_distance = lat_long_nearest_kitchen(lat,long)

        if  order_kitchen  ==  3276:
            data = {'message': 'Sorry we are not operating in your area'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        elif  order_kitchen  is None:
            data = {'message': 'Sorry there is no kitchen at the moment to serve your order'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)



        order_fcm = request.data.get('order_fcm') 
        print("order_fcm",order_fcm)
        if order_fcm is None:
            data = {'message': 'Please Enter Fcm token'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        
         


        customer_email = request.data.get('customer_email') or None
        if customer_email is None:
            # print("Please Enter  customer email")
            # daily_items_cart_error = True
            data = {'message': 'Please Enter customer  email'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST) 
        
        subscription_info = request.data.get('subscription_info') or None
        print("subscription_info",subscription_info)


        contact = request.data.get('contact')
        # print("contact",contact)
        if contact is None:
            # print("Please Enter  contact number")
            # daily_items_cart_error = True
            data = {'message': 'Please Enter  contact number'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

        is_cod = request.data.get('is_cod')
        # print("is_cod",is_cod)
        if is_cod is None:
            # print("Please Enter  contact is_cod")
            # daily_items_cart_error = True
            data = {'message': 'Please Enter  is_cod'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

        customer_name = request.data.get('customer_name') or None
        if customer_name is None:
            # print("Please Enter  customer name")
            # daily_items_cart_error = True
            data = {'message': 'Please Enter customer name'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

         
        order_details = request.data.get('order_details')  
        # print("order_details",order_details)
        if order_details is None:
            # print("Please Enter  order details")
            # daily_items_cart_error = True
            data = {'message': 'Please Enter order details'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

        selected_addon_ids = request.data.get('selected_addon') or None
        print("selected_addon_ids",selected_addon_ids)
        if selected_addon_ids is None:
            pass
        else:
            if  not len(selected_addon_ids):
                # print("Add on cannot be empty")
                # daily_items_cart_error = True
                data = {'message': 'Add on cannot be empty'}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        total_price = request.data.get('total_price') or None
        if total_price is None:
            # print("Please Enter total price")
            # daily_items_cart_error = True
            data = {'message': 'Please Enter total price'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        
        daily_items_cart = request.data.get('daily_items_cart')
        print("daily_items_cart",daily_items_cart,type(daily_items_cart))
        if  daily_items_cart is None:
            data = {'message': 'Please Enter daily items cart'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

        if  isinstance(daily_items_cart, list):
            pass
        else:
            data = {'message': 'Please Enter daily items cart is a list'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

        menu_items_cart = request.data.get('menu_items_cart')
        print("menu_items_cart",menu_items_cart,type(menu_items_cart))
        if  menu_items_cart is None:
            data = {'message': 'Please Enter menu items cart'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

        if  isinstance(menu_items_cart, list):
            pass
        else:
            data = {'message': 'Please Enter menu items cart is a list'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

        deals_cart = request.data.get('deals_cart')
        print("deals_cart",deals_cart,type(deals_cart))
        if  deals_cart is None:
            #deals_cart = []
            data = {'message': 'Please Enter deals cart'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

        if  isinstance(deals_cart, list):
            pass
        else:
            data = {'message': 'Please Enter deals cart is a list'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        
        

        if  len(daily_items_cart)   or  len(menu_items_cart) or  len(deals_cart):

            order_instance = Orders.objects.create(user = customer_email,kitchen_to_customer_distance=the_distance,order_details=order_details,subscription_info=subscription_info,contact=contact,is_cod=is_cod,address_details=customer_address,latitude=lat,longitude=long, customer_name=customer_name,order_fcm=order_fcm, total_price=total_price,kitchen_id=order_kitchen)
            order_instance.save()

            has_menu = False 

            delete_order = False
            payment_percentages  = 0 

            if  len(deals_cart):
                deals_cart_error = False
                one_correct_deal = False
                
                
                for   data  in  deals_cart: 

                    deal_id =  data.get('deal_id') or None
                    if deal_id is None:
                        print("Please Enter deal  id")
                        deals_cart_error = True

                    
                    if  not  Deals.objects.filter(pk=deal_id).exists():
                        print("Please Enter  valid deal id")
                        deals_cart_error = True

                    
                    quantity =  data.get('quantity')
                    if quantity is None:
                        print("Please Enter deal quantity")
                        deals_cart_error = True

                    
                    deal_price =  data.get('deal_price') or None
                    if deal_price is None:
                        print("Please Enter deal price")
                        deals_cart_error = True


                    selected_addon_ids_local = data.get('selected_addon') or None
                    print("selected_addon_ids_local",selected_addon_ids_local)
                    if selected_addon_ids_local is None:
                        pass
                    else:
                        if  not len(selected_addon_ids_local):
                            print("Add on cannot be empty (local deals)")
                            deals_cart_error = True

                    if   not   deals_cart_error:
                        one_correct_deal  = True
                        orderdeal_instance = OrderDealItems.objects.create(order_id = order_instance.pk, deal_id = deal_id,  sub_total= float(deal_price) *  float(quantity),quantity=quantity)
                        orderdeal_instance.save()
                        #Adds on 
                        if selected_addon_ids_local is None:
                            pass
                        else:
                            if   any(isinstance(item, dict) for item in selected_addon_ids_local):
                                for   item  in selected_addon_ids_local:
                                    Dealsorderaddson.objects.create(quantity=item.get('quantity'),dealorder_item_id=orderdeal_instance.pk,orderdeal_addson_id=item.get('id'))
                                    OrderAddson.objects.create(order_id = order_instance.pk, item_id = item.get('id'), quantity =item.get('quantity'))

                            else:

                                # Original list of integers
                                integer_list =  selected_addon_ids_local

                                # Count the occurrences of each integer in the list
                                counts = Counter(integer_list)

                                # Create a list of tuples where each tuple is (integer, count)
                                result = [(num, count) for num, count in counts.items()]

                                print(result)
                                for item in result: 
                                    # print("id",item,type(item))
                                    # count = selected_addon_ids.count(str(item))
                                    # print("count",count)
                                    Dealsorderaddson.objects.create(quantity=item[1],dealorder_item_id=orderdeal_instance.pk,orderdeal_addson_id=item[0])
                                    OrderAddson.objects.create(order_id = order_instance.pk, item_id = item[0], quantity =item[1])  
        
            if  len(daily_items_cart):
                daily_items_cart_error = False
                one_correct_item = False
                
                
                for   data  in  daily_items_cart: 

                    item_id =  data.get('item_id') or None
                    if item_id is None:
                        print("Please Enter item  id")
                        daily_items_cart_error = True
                        # data = {'message': 'Please Enter item  id'}
                        # return Response(data, status=status.HTTP_400_BAD_REQUEST)
                    

                     

                    quantity =  data.get('quantity')
                    if quantity is None:
                        print("Please Enter  quantity")
                        daily_items_cart_error = True
                        # data = {'message': 'Please Enter  quantity'}
                        # return Response(data, status=status.HTTP_400_BAD_REQUEST)
                    

                     
                     
                    if  not  Menuitems.objects.filter(pk=item_id).exists():
                        print("Please Enter  valid item id")
                        daily_items_cart_error = True
                        # data = {'message': 'Please Enter valid item  id'}
                        # return Response(data, status=status.HTTP_400_BAD_REQUEST)

                    
                    
                    
                    
                    item_price =  data.get('item_price') or None
                    if item_price is None:
                        print("Please Enter   item price")
                        daily_items_cart_error = True
                        # data = {'message': 'Please Enter item  price'}
                        # return Response(data, status=status.HTTP_400_BAD_REQUEST)
                    
 
                    selected_addon_ids_local = data.get('selected_addon') or None
                    print("selected_addon_ids_local",selected_addon_ids_local)
                    if selected_addon_ids_local is None:
                        pass
                    else:
                        if  not len(selected_addon_ids_local):
                            print("Add on cannot be empty (local daily)")
                            daily_items_cart_error = True
                            # data = {'message': 'Add on cannot be empty'}
                            # return Response(data, status=status.HTTP_400_BAD_REQUEST)
                        
 
                    if   not   daily_items_cart_error:
                        one_correct_item  = True  

                        orderitem_instance = OrderItems.objects.create(order_id = order_instance.pk, item_id = item_id, sub_total= float(item_price) * float(quantity),quantity=quantity)
                        orderitem_instance.save()

                        #Adds on 
                        if selected_addon_ids_local is None:
                            pass
                        else:
                            if   any(isinstance(item, dict) for item in selected_addon_ids_local):
                                for   item  in selected_addon_ids_local:
                                    Itemsorderaddson.objects.create(quantity=item.get('quantity'),order_item_id=orderitem_instance.pk,orderitems_addson_id=item.get('id'))
                                    OrderAddson.objects.create(order_id = order_instance.pk, item_id = item.get('id'), quantity =item.get('quantity'))

                            else:

                                # Original list of integers
                                integer_list =  selected_addon_ids_local

                                # Count the occurrences of each integer in the list
                                counts = Counter(integer_list)

                                # Create a list of tuples where each tuple is (integer, count)
                                result = [(num, count) for num, count in counts.items()]

                                print(result)
                                for item in result: 
                                    # print("id",item,type(item))
                                    # count = selected_addon_ids.count(str(item))
                                    # print("count",count)
                                    Itemsorderaddson.objects.create(quantity=item[1],order_item_id=orderitem_instance.pk,orderitems_addson_id=item[0])
                                    OrderAddson.objects.create(order_id = order_instance.pk, item_id = item[0], quantity =item[1])   
             
            if  len(menu_items_cart): 
                menu_items_cart_error = False
                menu_correct_item = False
                for   data  in  menu_items_cart:
                    menu_id =  data.get('menu_id') or None
                    if menu_id is None:
                        print("Please Enter menu  id")
                        menu_items_cart_error = True
                        # data = {'message': 'Please Enter item  id'}
                        # return Response(data, status=status.HTTP_400_BAD_REQUEST)
                    

                     

                    quantity =  data.get('quantity')
                    if quantity is None:
                        print("Please Enter  quantity")
                        menu_items_cart_error = True
                        # data = {'message': 'Please Enter  quantity'}
                        # return Response(data, status=status.HTTP_400_BAD_REQUEST)
                    

                     
                     
                    if  not  Menu.objects.filter(pk=menu_id).exists():
                        print("Please Enter  valid menu id")
                        menu_items_cart_error = True
                        # data = {'message': 'Please Enter valid item  id'}
                        # return Response(data, status=status.HTTP_400_BAD_REQUEST)

                    
                    
                    
                    
                    menu_price =  data.get('menu_price') or None
                    if menu_price is None:
                        print("Please Enter  menu  price")
                        menu_items_cart_error = True
                        # data = {'message': 'Please Enter item  price'}
                        # return Response(data, status=status.HTTP_400_BAD_REQUEST)

                    selected_addon_ids_local = data.get('selected_addon') or None
                    print("selected_addon_ids_local",selected_addon_ids_local)
                    if selected_addon_ids_local is None:
                        pass
                    else:
                        if  not len(selected_addon_ids_local):
                            print("Add on cannot be empty (local menu)")
                            daily_items_cart_error = True
                            # data = {'message': 'Add on cannot be empty'}
                            # return Response(data, status=status.HTTP_400_BAD_REQUEST)
                    
  
 
                    if   not   menu_items_cart_error:
                        menu_correct_item  = True  

                        ordermenu_instance = OrderMenuItems.objects.create(order_id = order_instance.pk, menu_id = menu_id,  sub_total= float(menu_price) *  float(quantity),quantity=quantity)
                        ordermenu_instance.save()


                        #Adds on 
                        if selected_addon_ids_local is None:
                            pass
                        else:
                            if   any(isinstance(item, dict) for item in selected_addon_ids_local):
                                for   item  in selected_addon_ids_local:
                                    Menuorderaddson.objects.create(quantity=item.get('quantity'),menuorder_item_id=ordermenu_instance.pk,ordermenu_addson_id=item.get('id'))
                                    OrderAddson.objects.create(order_id = order_instance.pk, item_id = item.get('id'), quantity =item.get('quantity'))

                            else:

                                # Original list of integers
                                integer_list =  selected_addon_ids_local

                                # Count the occurrences of each integer in the list
                                counts = Counter(integer_list)

                                # Create a list of tuples where each tuple is (integer, count)
                                result = [(num, count) for num, count in counts.items()]

                                print(result)
                                for item in result: 
                                    # print("id",item,type(item))
                                    # count = selected_addon_ids.count(str(item))
                                    # print("count",count)
                                    Menuorderaddson.objects.create(quantity=item[1],menuorder_item_id=ordermenu_instance.pk,ordermenu_addson_id=item[0])
                                    OrderAddson.objects.create(order_id = order_instance.pk, item_id = item[0], quantity =item[1])   

                        # menu_instance = Menu.objects.filter(pk=menu_id).first()

                        # if     MenuCategory.objects.filter(pk=menu_instance.category_id).exclude(Kitchen_share_percent=None).exists():
                        #     menu_ins  =  MenuCategory.objects.filter(pk=menu_instance.category_id).first() 
                            
                        #     try:
                        #         payment_percentages = payment_percentages +   menu_ins.Kitchen_share_percent 
                        #     except:
                        #         payment_percentages = payment_percentages +   10
                        # else:
                        #     payment_percentages = payment_percentages + 10 

                        

            cart_mesage = ""
            if  len(daily_items_cart):
                if  daily_items_cart_error:
                    delete_order = True
                    if  one_correct_item:
                        cart_mesage = 'Incorrect  data was sent in daily  cart items but at least on cart item was correct'
                    else:
                        cart_mesage = 'Incorrect  data was sent in daily  cart items'
                else:  
                    pass
                    # if     MenuCategory.objects.filter(menu_count=1).exclude(Kitchen_share_percent=None).exists():
                    #     payment_percentage  =  MenuCategory.objects.filter(menu_count=1).first()
                    #     try:
                    #         payment_percentages = payment_percentages +  payment_percentage.Kitchen_share_percent
                    #     except:
                    #         payment_percentages = payment_percentages + 10  
                    # else: 
                    #     payment_percentages = payment_percentages + 10 
 

            if  len(deals_cart):
                if  deals_cart_error:
                    delete_order = True
                    if  one_correct_deal:
                        cart_mesage = cart_mesage  +  '(    Incorrect  data was sent in deal  cart items but at least on cart item was correct)'
                    else:
                        cart_mesage = cart_mesage +  '(    Incorrect  data was sent in deal  cart items)'
            
            if  len(menu_items_cart):
                if  menu_items_cart_error:
                    delete_order = True
                    if  menu_correct_item:
                        cart_mesage = cart_mesage  +  '(    Incorrect  data was sent in menu  cart items but at least on cart item was correct)'
                    else:
                        cart_mesage = cart_mesage +  '(    Incorrect  data was sent in daily  cart items)'
                else:
                    has_menu = True 
            
            if  delete_order:
                order_instance.delete()
                data = {'message':cart_mesage }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            else:
                #Adds on 
                # if selected_addon_ids is None:
                #     pass
                # else:
                #     if   any(isinstance(item, dict) for item in selected_addon_ids):
                #         for   item  in selected_addon_ids:
                #             OrderAddson.objects.create(order_id = order_instance.pk, item_id = item.get('id'), quantity =item.get('quantity'))

                #     else:

                #         # Original list of integers
                #         integer_list =  selected_addon_ids

                #         # Count the occurrences of each integer in the list
                #         counts = Counter(integer_list)

                #         # Create a list of tuples where each tuple is (integer, count)
                #         result = [(num, count) for num, count in counts.items()]

                #         print(result)
                #         for item in result: 
                #             # print("id",item,type(item))
                #             # count = selected_addon_ids.count(str(item))
                #             # print("count",count)
                #             OrderAddson.objects.create(order_id = order_instance.pk, item_id = item[0], quantity =item[1]) 

                order_instance.has_menu = has_menu
                status_code = Orderstatus.objects.filter(is_pending=True).first()
                order_instance.its_color_code = status_code.its_color_code
                order_instance.status = status_code.status_title
                order_instance.save()
                try:
                    #Send WebSocket notification
                    async_to_sync(channel_layer.group_send)(
                        'orders_listing_group',
                        {
                            'type': 'send_order_list_notification',
                            'message': f'Order {order_instance.pk} has been submitted!'
                        }
                    )
                    print("webscoket  have updated agent orders list")
                except:
                    print("webscoket  amybe closed")



                #Kitchen payments

                try:
                    kitchen_perc = FoodappSettings.objects.last()
                    kitchen_share_amount = float(kitchen_perc.Kitchen_share_percent)/float(100)   *  float(total_price)
                    print("kitchen_share_amount",kitchen_share_amount)
                    print("kitchen_share_amount",truncate_float(kitchen_share_amount,2))
                
                    kitchenOrdersPayment.objects.create(
                        Kitchen_id = order_kitchen, 
                        order_id =  order_instance.pk,
                        kitchen_share_amount =   truncate_float(kitchen_share_amount,2)
                    )
                except:
                    kitchen_share_amount = float(10/100)   * float(total_price)
                    print("into percentage exception")
                    print("kitchen_share_amount",kitchen_share_amount)
                    print("kitchen_share_amount",truncate_float(kitchen_share_amount,2))
                    kitchenOrdersPayment.objects.create(
                        Kitchen_id = order_kitchen, 
                        order_id =  order_instance.pk,
                        kitchen_share_amount =   truncate_float(kitchen_share_amount,2)
                    )


                data = {'message': 'cart  submitted successfully','order_id':order_instance.pk,'total_price':total_price}
                return Response(data, status=status.HTTP_200_OK)
        else:

            data = {'message': 'Both  daily and menu items cart was empty'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST) 
        



#Get my all Orders 
class  GetmyallOrders(APIView):
    def  get(self,request,my_email):
        if   Orders.objects.filter(user=my_email).exists():
            serialized_data = MyallordersSerializer(Orders.objects.filter(user=my_email),many=True)
            return Response(serialized_data.data,status=status.HTTP_200_OK)
        else:
            return Response(data={'message':"No orders found for this user"},status=status.HTTP_404_NOT_FOUND)



# Search APi
class  GetSearch(APIView): 
    def  get(self,request,key):
        content = {'is_record':False} 
        if  Menuitems.objects.filter(title__icontains=key).filter(ads_on=False).exists():  
            content['items'] = DailyMenuitemsSerializer(Menuitems.objects.filter(title__icontains=key).filter(ads_on=False),many=True).data
            content['is_record'] =  True

        if  Menu.objects.filter(title__icontains=key).exclude(category_id__in=list(MenuCategory.objects.filter(menu_count=1).values_list('pk',flat=True))).exists():  
            content['Menus'] = MenuSerializer(Menu.objects.filter(title__icontains=key).exclude(category_id__in=list(MenuCategory.objects.filter(menu_count=1).values_list('pk',flat=True))),many=True).data
            content['is_record'] =  True


        if  Deals.objects.filter(title__icontains=key).exists():  
            content['Deals'] = DealsSerializer(Deals.objects.filter(title__icontains=key),many=True).data
            content['is_record'] =  True    

        

        return Response(content, status=status.HTTP_200_OK)
    


# Newsletter Api 
from  webApp.utils import *
class  Newsletter(APIView):
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.method != 'POST':
            content = {'message': "Please Enter Post method"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        newsletter_email = request.data.get('newsletter_email') or None 
        if newsletter_email is None:
            content = {'message': "Please Enter email!"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        if NewsletterRecords.objects.filter(email = newsletter_email).exists():
            content = {'message': "Email already recorded!"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
                          
        if newsletter_email:
            try: 
                if  not  verify_email_smtp(newsletter_email):
                    print("pas 1")
                    data = {'message': 'Invalid email!'}
                    return Response(data, status=status.HTTP_400_BAD_REQUEST) 
            except:
                pass
        
        NewsletterRecords.objects.create(email= newsletter_email)
        print("newsletter email ", newsletter_email)
        
        content = {'message': "Email recorded successfully!"}
        return Response(content, status=status.HTTP_200_OK)
    

#Get Deals
class GetDeals(APIView): 
    def  get(self,request):

        if  not  Deals.objects.filter(deal_items__isnull=False).exists():
            data = {'message': 'No deals exists !'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(DealsSerializer(Deals.objects.filter(deal_items__isnull=False).distinct(),many=True).data, status=status.HTTP_200_OK)