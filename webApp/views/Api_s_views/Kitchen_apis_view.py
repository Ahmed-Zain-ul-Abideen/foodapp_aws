from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from webApp.models import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  
from webApp.Serializers.Food_api_serializer import *
from webApp.views.Others.geocode_address import *
from  webApp.utils import *
from webApp.Serializers.kitchen_api_serializer  import *
from django.db.models import Count
from datetime import date
from django.shortcuts import get_object_or_404


#KitchenPaymentsApi
class  KitchenPaymentsApi(APIView): 
    permission_classes = (IsAuthenticated,)
    def  post(self, request,user_id):  
        # user_id = request.data.get('user_id') or None
        print("user_id",user_id)
        if user_id is None:
            data = {'message': 'Please Enter user id'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        if  not   User.objects.filter(pk=user_id).exists():
            data = {'message': 'Please Enter valid user id'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

        if  not  Kitchen.objects.filter(approved_owner_id=user_id).exists():
            data = {'message': 'Kitchen does not exist for this user'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

        iban_number = request.data.get('iban_number') or None
        print("iban_number",iban_number)
        if iban_number is None:
            data = {'message': 'Please Enter iban number'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

        account_title = request.data.get('account_title') or None
        print("account_title",account_title)
        if account_title is None:
            data = {'message': 'Please Enter account title'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

        bank_name = request.data.get('bank_name') or None
        print("bank_name",bank_name)
        if bank_name is None:
            data = {'message': 'Please Enter bank name'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

        if   Paymentaccounts.objects.filter(user_id=user_id).exists():
            payment_account_instance = Paymentaccounts.objects.filter(user_id=user_id).last()
            payment_account_instance.iban_number = iban_number
            payment_account_instance.account_title = account_title
            payment_account_instance.bank_name = bank_name
            payment_account_instance.save()
            data = {'message': 'Kitchen payment account info updated successfully !'}
            return Response(data, status=status.HTTP_200_OK)
        else:
            Paymentaccounts.objects.create(
                user_id=user_id,
                iban_number=iban_number,
                account_title=account_title,
                bank_name=bank_name
            )
            data = {'message': 'Kitchen payment account info added successfully !'}
            return Response(data, status=status.HTTP_201_CREATED)
        
    def  get(self,request,user_id):
        print("user_id",user_id)
        if  not  Kitchen.objects.filter(approved_owner_id=user_id).exists():
            data = {'message': 'User kitchen doesnot exist'}
            return Response(data, status=status.HTTP_303_SEE_OTHER)
        elif not  Paymentaccounts.objects.filter(user_id=user_id).exists():
            data = {'message': 'User  payment account does not exist !'}
            return Response(data, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return  Response(KitchenPaymentsApiSerializer(Paymentaccounts.objects.filter(user_id=user_id).last()).data,
                status=status.HTTP_200_OK
            )

        
         

#Save  Kitchen
class  SaveKitchen(APIView): 
    permission_classes = (IsAuthenticated,)
    def  post(self, request): 
        
        user_id = request.data.get('user_id') or None
        print("user_id",user_id)
        if user_id is None:
            print("400  2")
            data = {'message': 'Please Enter user id'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        if  not   User.objects.filter(pk=user_id).exists(): 
            print("400  3")
            data = {'message': 'Please Enter valid user id'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

        if   Kitchen.objects.filter(approved_owner_id=user_id).exists():
            print("kitchen already exist")
            data = {'message': 'Kitchen already exist for this user'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        

        address_details = request.data.get('address_details') or None

        if address_details is None:
            data = {'message': 'Please Enter kitchen address'}
            print("400  1")
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        
        lat = None
        try:
            lat, long = OpenCage_for_address(address_details)
        except: 
            print("400  4")
            data = {'message': 'This address cannot be traced please enter valid one  !'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)  
        
        
        if lat is None:
            print("400  5")
            data = {'message': 'This address cannot be located please enter valid one  !'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST) 
        

        email = request.data.get('email') or None
        print("email",email)
        if email is None:
            print("400  6")
            data = {'message': 'Please Enter email'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        try: 
            if  not  verify_email_smtp(email):
                print("pas 1")
                data = {'message': 'This email is not deliverable !'}
                return Response(data, status=status.HTTP_400_BAD_REQUEST) 
        except:
            pass

        kitchen_title = request.data.get('kitchen_title') or None
        print("kitchen_title",kitchen_title)

        if kitchen_title is None:
            print("400  8")
            data = {'message': 'Please Enter kitchen title'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        if Kitchen.objects.filter(name = kitchen_title).exists():
            data = {'message': 'Kitchen title already exists'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        


        owner_name = request.data.get('owner_name') or None
        print("owner_name",owner_name)

        if owner_name is None:
            print("400  9")
            data = {'message': 'Please Enter owner name'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        contact_number = request.data.get('contact_number') or None
        print("contact_number",contact_number)

        if contact_number is None:
            print("400  10")
            data = {'message': 'Please Enter  contact number'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


        kitchen_images = request.FILES.getlist('kitchen_images')
        print("im ab",kitchen_images)
        # kitchen_images = request.data.get('kitchen_images')
        # print("im bel",kitchen_images)

        if kitchen_images is None:
            print("400  11")
            data = {'message': 'Please Enter kitchen images'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

        
        elif  kitchen_images:
            print("llllll") 
            for image in kitchen_images:

                file_extension = image.name.split('.')[-1].lower() 
                print(file_extension)
            
                if file_extension in ['png', 'jpg', 'jpeg']:
                    pass
                else: 
                    data = {'message': 'Uplaod images as png, jpg or jpeg  file Only !'}
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
                

            try:
                kitchen_admin = lat_long_nearest_admin(lat,long)
            except:
                kitchen_admin = None

            kitchen_instance = Kitchen.objects.create(kitchen_admin=kitchen_admin,approved_owner_id=user_id,name= kitchen_title, owner= owner_name , contact = contact_number, email = email)

            kitchen_instance.save()

            KitchenAddress.objects.create(Kitchen_id=kitchen_instance.pk,address_details=address_details,latitude=lat,longitude=long)

            # KitchenMedia.objects.create(Kitchen_id = kitchen_instance.pk ,file=kitchen_images)

            # data = {'message': 'Kitchen request submitted succesfully'}
            # return Response(data, status=status.HTTP_200_OK)
                
            for image in kitchen_images:
                KitchenMedia.objects.create(Kitchen_id = kitchen_instance.pk ,file=image)

            data = {'message': 'Kitchen registered successfully'}
            return Response(data, status=status.HTTP_200_OK)

        else:
            data = {'message': 'Please Enter at least one   image for kitchen'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


#Kitchen  Active/Inactive
class  SaveKitchenavailblity(APIView): 
    permission_classes = (IsAuthenticated,)
    def  post(self, request):

        kitchen_id = request.data.get('kitchen_id') or None
        if kitchen_id is None:
            print("400 av 1")
            data = {'message': 'Please Enter kitchen id'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        if not  Kitchen.objects.filter(pk=kitchen_id).exists():
            print("400 av  2")
            data = {'message': 'Please Enter valid kitchen id'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        active_inactive = request.data.get('active_inactive')
        print("active_inactive",active_inactive)
        if active_inactive is None:
            print("400 av 3")
            data = {'message': 'Please Enter kitchen availblity is True or False'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        # if  Kitchen.objects.filter(pk=kitchen_id).filter(is_active=True).exists():
        #     Kitchen.objects.filter(pk=kitchen_id).update(is_active=False)
        # else:
        print("acttt",active_inactive,type(active_inactive))
        Kitchen.objects.filter(pk=kitchen_id).update(is_active=active_inactive)

        data = {'message': 'Kitchen availblity updated successfully'}
        return Response(data, status=status.HTTP_200_OK)

#Update  Kitchen
class  SaveKitchenSpeciality(APIView): 
    permission_classes = (IsAuthenticated,)
    def  post(self, request):

        kitchen_id = request.data.get('kitchen_id') or None
        if kitchen_id is None:
            print("400 av 1")
            data = {'message': 'Please Enter kitchen id'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

        speciality_items = request.data.get('speciality_items') or None
        if speciality_items is None:
            data = {'message': 'Please Enter kitchen  speciality items'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        if  not len(speciality_items):
            data = {'message': 'Speciality items cannot be empty'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        if not  Kitchen.objects.filter(pk=kitchen_id).exists():
            data = {'message': 'Please Enter valid kitchen id'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

        if KitchenSpeciality.objects.filter(Kitchen_id=kitchen_id).exists():
            kitchen_speciality_items = KitchenSpeciality.objects.filter(Kitchen_id=kitchen_id).first()
            kitchen_speciality_items_list = json.decoder.JSONDecoder().decode(kitchen_speciality_items.items)

            for id in speciality_items:
                if int(id) in kitchen_speciality_items_list:
                    kitchen_speciality_items_list.remove(int(id))
                else:
                    kitchen_speciality_items_list.append(int(id))

            kitchen_speciality_items.items = json.dumps(kitchen_speciality_items_list)
        else:
            kitchen_speciality_items = KitchenSpeciality.objects.create(Kitchen_id=kitchen_id,items=json.dumps(speciality_items))
        
        kitchen_speciality_items.save() 

        data = {'message': 'Kitchen Specialities updated successfully'}
        return Response(data, status=status.HTTP_200_OK)


#Update  Kitchen
class  UpdateKitchen(APIView): 
    permission_classes = (IsAuthenticated,)
    def  post(self, request):


        kitchen_id = request.data.get('kitchen_id') or None
        if kitchen_id is None:
            data = {'message': 'Please Enter kitchen id'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        if not  Kitchen.objects.filter(pk=kitchen_id).exists():
            data = {'message': 'Please Enter valid kitchen id'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        kitchen_instance = Kitchen.objects.filter(pk=kitchen_id).first()

        address_details = request.data.get('address_details') or None

        if address_details is None:
            pass
        else: 
        
            lat = None
            
            if KitchenAddress.objects.filter(address_details=address_details).exists():
                pass
            else:  
                try:
                    lat, long = OpenCage_for_address(address_details)
                except: 
                    data = {'message': 'This address cannot be traced please enter valid one  !'}
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)  
                
                
                if lat is None:
                    data = {'message': 'This address cannot be located please enter valid one  !'}
                    return Response(data, status=status.HTTP_400_BAD_REQUEST) 
                

                try:
                    kitchen_admin = lat_long_nearest_admin(lat,long)
                except:
                    kitchen_admin = None

                kitchen_instance.kitchen_admin = kitchen_admin
                
                kitchen_address_instance = KitchenAddress.objects.filter(kitchen_id=kitchen_id).first()
                kitchen_address_instance.address_details = address_details
                kitchen_address_instance.latitude = lat
                kitchen_address_instance.longitude = long
                kitchen_address_instance.save()

        
        email = request.data.get('email') or None

        if email is None:
            pass
        else: 
            if Kitchen.objects.filter(email=email).exists():
                pass
            else:  
                if  verify_email_smtp(email):
                    kitchen_instance.email = email
                else:
                    data = {'message': 'This email is not deliverable !'}
                    return Response(data, status=status.HTTP_400_BAD_REQUEST) 
                

        kitchen_title = request.data.get('kitchen_title') or None

        if kitchen_title is None:
            pass
        else:
            kitchen_instance.name = kitchen_title

        owner_name = request.data.get('owner_name') or None

        if owner_name is None:
            pass
        else:
            kitchen_instance.owner = owner_name
        
        contact_number = request.data.get('contact_number') or None

        if contact_number is None:
            pass
        else:
            kitchen_instance.contact = contact_number


        kitchen_images = request.FILES.getlist('kitchen_images') or None

        if kitchen_images is None:
            pass 
        elif  kitchen_images:

            for image in kitchen_images:

                file_extension = image.name.split('.')[-1].lower() 
            
                if file_extension in ['png', 'jpg', 'jpeg']:
                    pass
                else: 
                    data = {'message': 'Uplaod images as png, jpg or jpeg  file Only !'}
                    return Response(data, status=status.HTTP_400_BAD_REQUEST) 
                
                
            for image in kitchen_images:
                KitchenMedia.objects.create(Kitchen_id = kitchen_instance.pk ,file=image)

        else:
            pass

        kitchen_instance.save()


        data = {'message': 'Kitchen updated successfully !'}
        return Response(data, status=status.HTTP_200_OK) 



#Get My Kitchen Details 
class GetMyKitchenDetails(APIView):
    permission_classes = (IsAuthenticated,)
    def  get(self,request,user_id):

        if  not  Kitchen.objects.filter(approved_owner_id=user_id).exists():
            data = {'message': 'User kitchen doesnot exist'}
            return Response(data, status=status.HTTP_303_SEE_OTHER)
        else:
            return  Response(KitchenDeatilsSerializer(Kitchen.objects.filter(approved_owner_id=user_id).first()).data,
                status=status.HTTP_200_OK
            )
        

#Get My Kitchen Orders
class GetMyKitchenOrders(APIView):
    permission_classes = (IsAuthenticated,)
    def  get(self,request,user_id):

        if  not  Kitchen.objects.filter(approved_owner_id=user_id).exists():
            data = {'message': 'User kitchen doesnot exist'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            user_kitchen_id = list(Kitchen.objects.filter(approved_owner_id=user_id).values_list('pk',flat=True)) 
            if  not  Orders.objects.annotate(menu_orders_count=Count('order_menu_items')).filter(menu_orders_count=0).filter(kitchen_id__in=user_kitchen_id).exclude(to_be_confirmed= True).exclude(is_cancelled= True).exclude(pk__in=list(OrderProcessedStatuses.objects.filter(status_id__in=list(Orderstatus.objects.filter(is_pickup=True).values_list('pk',flat=True))).values_list('order_id',flat=True))).exists():
                data = {'message': 'kitchen new  daily orders doesnot exist'}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            else: 
                return  Response(KitchenOrdersSerializer(Orders.objects.annotate(menu_orders_count=Count('order_menu_items')).filter(menu_orders_count=0).filter(kitchen_id__in=user_kitchen_id).exclude(to_be_confirmed= True).exclude(is_cancelled= True).exclude(pk__in=list(OrderProcessedStatuses.objects.filter(status_id__in=list(Orderstatus.objects.filter(is_pickup=True).values_list('pk',flat=True))).values_list('order_id',flat=True))),many=True).data,
                    status=status.HTTP_200_OK
                )
            

#Get My Kitchen Cooked Orders
class GetMyKitchenCookedOrders(APIView):
    permission_classes = (IsAuthenticated,)
    def  get(self,request,user_id):

        if  not  Kitchen.objects.filter(approved_owner_id=user_id).exists():
            data = {'message': 'User kitchen doesnot exist'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            user_kitchen_id = list(Kitchen.objects.filter(approved_owner_id=user_id).values_list('pk',flat=True))
            today= date.today() 
            if  not  Orders.objects.filter(kitchen_id__in=user_kitchen_id).filter(to_be_confirmed=False).filter(pk__in=list(OrderProcessedStatuses.objects.filter(processed_date__lte=today).filter(status_id__in=list(Orderstatus.objects.filter(is_pickup=True).values_list('pk',flat=True))).values_list('order_id',flat=True))).exists():
                data = {'message': 'kitchen cooked  daily orders doesnot exist'}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            else: 
                return  Response(KitchenallcookedOrdersSerializer(Orders.objects.filter(kitchen_id__in=user_kitchen_id).filter(to_be_confirmed=False).filter(pk__in=list(OrderProcessedStatuses.objects.filter(processed_date__lte=today).filter(status_id__in=list(Orderstatus.objects.filter(is_pickup=True).values_list('pk',flat=True))).values_list('order_id',flat=True))),many=True).data,
                    status=status.HTTP_200_OK
                )
        

#Get My Kitchen Menu Orders
class GetMyKitchenMenuOrders(APIView):
    permission_classes = (IsAuthenticated,)
    def  get(self,request,user_id):

        if  not  Kitchen.objects.filter(approved_owner_id=user_id).exists():
            data = {'message': 'User kitchen doesnot exist'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            user_kitchen_id = list(Kitchen.objects.filter(approved_owner_id=user_id).values_list('pk',flat=True))
            if  not  Orders.objects.annotate(menu_orders_count=Count('order_menu_items')).exclude(menu_orders_count=0).filter(kitchen_id__in=user_kitchen_id).filter(to_be_confirmed=False).exists():
                data = {'message': 'kitchen menu orders doesnot exist'}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            else: 
                return  Response(MenuOrdersSerializer(Orders.objects.annotate(menu_orders_count=Count('order_menu_items')).exclude(menu_orders_count=0).filter(kitchen_id__in=user_kitchen_id).filter(to_be_confirmed=False),many=True).data,
                    status=status.HTTP_200_OK
                )
            

#Get Kitchen Order statuses
class  GetKitchenOrderstatuses(APIView): 
    def  get(self,request):

        if  not  Orderstatus.objects.filter(role='Kitchen').exists():
            data = {'message': 'No records found'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return  Response(OrderstatusSerializer(Orderstatus.objects.filter(role='Kitchen'),many=True).data,
                status=status.HTTP_200_OK
            )
        

#Get Single Food Item
class GetSingleFoodItems(APIView):
    def  get(self,request,id):
        if Menuitems.objects.filter(id=id).exists():
            serialized_data = DailyMenuitemsSerializer(Menuitems.objects.filter(id=id).first())
            return Response(serialized_data.data,status=status.HTTP_200_OK)
        else:
            return Response(data={'message':"No item found"},status=status.HTTP_400_BAD_REQUEST)
        


#Get Kitchen Orders Payments 
class   GetKitchenOrdersPayments(APIView):
    permission_classes = (IsAuthenticated,)
    def  get(self,request,kitchen_id):
        today= date.today() 
        if  not  Kitchen.objects.filter(pk=kitchen_id).exists():
            data = {'message': 'kitchen doesnot exist'}
            return Response(data, status=status.HTTP_303_SEE_OTHER)
        elif   not   Orders.objects.filter(kitchen_id=kitchen_id).filter(to_be_confirmed=False).exists():
            data = {'message': 'No  orders yet, so no payments for the kitchen yet'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        elif   not  kitchenOrdersPayment.objects.filter(Kitchen_id=kitchen_id).filter(order_id__in=list(Orders.objects.filter(kitchen_id=kitchen_id).filter(to_be_confirmed=False).filter(pk__in=list(OrderProcessedStatuses.objects.filter(processed_date__lte=today).filter(status_id__in=list(Orderstatus.objects.filter(is_pickup=True).values_list('pk',flat=True))).values_list('order_id',flat=True))))).exists():
            data = {'message': 'orders  exist for kitchen, but payments  not confirmed yet'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return  Response(kitchenOrdersPaymentSerializer(kitchenOrdersPayment.objects.filter(Kitchen_id=kitchen_id).filter(order_id__in=list(Orders.objects.filter(kitchen_id=kitchen_id).filter(to_be_confirmed=False).filter(pk__in=list(OrderProcessedStatuses.objects.filter(processed_date__lte=today).filter(status_id__in=list(Orderstatus.objects.filter(is_pickup=True).values_list('pk',flat=True))).values_list('order_id',flat=True))))),many=True).data,
                status=status.HTTP_200_OK
            )
        

#Get Kitchen Orders Payments  Updated
class   GetKitchenOrdersPaymentsUpdated(APIView):
    permission_classes = (IsAuthenticated,)
    def  get(self,request,kitchen_id):
        today= date.today() 
        if  not  Kitchen.objects.filter(pk=kitchen_id).exists():
            data = {'message': 'kitchen doesnot exist'}
            return Response(data, status=status.HTTP_303_SEE_OTHER)
        elif   not   Orders.objects.filter(kitchen_id=kitchen_id).filter(to_be_confirmed=False).exists():
            data = {'message': 'No  orders yet, so no payments for the kitchen yet'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        elif   not  kitchenOrdersPayment.objects.filter(Kitchen_id=kitchen_id).filter(is_payable=True).exists():
            data = {'message': 'orders  exist for kitchen, but payments  not processed yet'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return  Response(kitchenOrdersPaymentSerializer(kitchenOrdersPayment.objects.filter(Kitchen_id=kitchen_id).filter(is_payable=True),many=True).data,
                status=status.HTTP_200_OK
            )
        

#Rider Delivery Payments
class   GetRiderDeliveryPayments(APIView):
    permission_classes = (IsAuthenticated,)
    def  get(self,request,email):
        today= date.today() 
        if  not  RiderDetails.objects.filter(email=email).exists():
            data = {'message': 'Rider doesnot exist'}
            return Response(data, status=status.HTTP_303_SEE_OTHER)
        
        rider_id = get_object_or_404(RiderDetails.objects.only('id'), email=email)
        if   not  RiderDeliveryPayment.objects.filter(rider_id=rider_id.pk).filter(is_payable=True).exists():
            data = {'message': 'Rider delivered deliveries not exist!'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return  Response(RiderDeliveryPaymentSerializer(RiderDeliveryPayment.objects.filter(rider_id=rider_id.pk).filter(is_payable=True),many=True).data,
                status=status.HTTP_200_OK
            )

#Get My Kitchen all Orders
class  GetMyKitchenCurrentallOrders(APIView):
    permission_classes = (IsAuthenticated,)
    def  get(self,request,user_id):

        if  not  Kitchen.objects.filter(approved_owner_id=user_id).exists():
            data = {'message': 'User kitchen doesnot exist'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            user_kitchen_id = list(Kitchen.objects.filter(approved_owner_id=user_id).values_list('pk',flat=True)) 
            today = date.today()
            if  not  Orders.objects.filter(kitchen_id__in=user_kitchen_id).filter(to_be_confirmed=False).filter(is_cancelled=False).filter(kitchen_pickup_date__lte=today).filter(is_delivered=False).exclude(last_date_to_deliver__lt=today).exists():
                data = {'message': 'Orders doesnot exist'}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            else: 
                return  Response(KitchenCurrentallOrdersSerializer(Orders.objects.filter(kitchen_id__in=user_kitchen_id).filter(to_be_confirmed=False).filter(is_cancelled=False).filter(kitchen_pickup_date__lte=today).filter(is_delivered=False).exclude(last_date_to_deliver__lt=today).order_by('-id'),many=True).data,
                    status=status.HTTP_200_OK
                )