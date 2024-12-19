from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from webApp.models import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  
from rest_framework_simplejwt.tokens import RefreshToken 
from fcm_django.models import FCMDevice 
from webApp.Serializers.food_app_settings_seializers import *
from webApp.views.Others.geocode_address  import  *
from  webApp.Serializers.User_api_serializer  import  *
from django.db.models import Case,When
from django.shortcuts import get_object_or_404

#Get Payment Settings
class   GetPaymentSettings(APIView): 
    def  get(self,request): 
        return  Response(GetPaymentSettingsSerializer({'mange':'success'}).data.get('data'),
            status=status.HTTP_200_OK
        )
        # return  Response(GetPaymentSettingsSerializer(FoodappSettings.objects.last()).data,
        #     status=status.HTTP_200_OK
        # )

def get_username_from_mail(email):
    # Split the email address at '@' and return the part before it
    return email.split('@')[0]


class GetTokStatus(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,*args, **kwargs):
        return Response({"message":"success"}, status=status.HTTP_200_OK)

# Verify Kitchen
class VerifyKitchen(APIView): 
    def post(self, request):
        if request.method != 'POST':
            data = {'message': 'Please Enter Post method !'}
            return Response(data, status=status.HTTP_403_FORBIDDEN) 
        
        
        username = request.data.get('username') or None
        if username is None:
            data = {'message': 'Please Enter username'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)   
        

        password = request.data.get('password') or None
        if password is None:
            data = {'message': 'Please Enter password'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        confirm_password = request.data.get('confirm_password') or None
        if confirm_password is None:
            data = {'message': 'Please Enter confirm password'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

        if str(password)  !=  str(confirm_password):
            data = {'message': 'password  and  confirm password doesnot match'}
            return Response(data, status=status.HTTP_409_CONFLICT)
        
        fcm_token = request.data.get('fcm_token')   
        if fcm_token is None: 
            data = {'message':'Invalid Request, Missing FCM Token'}
            return Response(data,status=status.HTTP_409_CONFLICT)
        elif not fcm_token: 
            data = {'message':'Invalid Request,FCM Token is passed as an Empty string'}
            return Response(data,status=status.HTTP_409_CONFLICT)
        else:
            pass  


        user = authenticate(username=username,password=confirm_password)

        if   user is not None:
            this_user = User.objects.filter(username=username).first()
            token = RefreshToken.for_user(this_user)
            referesh = str(token)
            access_token = str(token.access_token) 


            if  Kitchen.objects.filter(approved_owner_id=this_user.pk).filter(is_active=False).exists():
                Kitchen.objects.filter(approved_owner_id=this_user.pk).filter(is_active=False).update(is_active=True)

            if   FCMDevice.objects.filter(registration_id=fcm_token).exists():

                #FCM Devices duplication handling start 
                if   FCMDevice.objects.filter(registration_id=fcm_token).filter(active=True).exclude(user_id__exact=this_user.pk).exists():
                    print("this device has duplicates this profile exist",fcm_token)
                    duplicates = FCMDevice.objects.filter(registration_id=fcm_token).filter(active=True).exclude(user_id__exact=this_user.pk)
                    for duplicate in duplicates:
                        print("duplicate user",duplicate.user_id)
                        duplicate.active = False
                        duplicate.save()

                #FCM Devices duplication handling end 

                if   FCMDevice.objects.filter(registration_id=fcm_token).filter(user_id__exact=this_user.pk).exists():
                    #if this device is inactive against this user then activate
                    if  FCMDevice.objects.filter(registration_id=fcm_token).filter(active=False).filter(user_id__exact=this_user.pk).exists():
                        FCMDevice.objects.filter(registration_id=fcm_token).filter(active=False).filter(user_id__exact=this_user.pk).update(active=True) 
                else:
                    fcm = FCMDevice(
                        registration_id=fcm_token, user_id=this_user.pk
                    )
                    fcm.save()
            else:
                fcm = FCMDevice(
                    registration_id=fcm_token, user_id=this_user.pk
                )
                fcm.save()

            
            data = {'userId': this_user.pk, 
                'access_token': access_token, 'refresh_token': referesh
            }


        else: 

            spaces_info = check_spaces(username) 
            if  spaces_info[0]  or  spaces_info[1]  or  spaces_info[2]:
                data = {'message': 'Space in  username at start or end or in between characters is not allowed !'}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            
            if User.objects.filter(username=username).exists():
                return Response({'message':"This username is already taken so enter correct credentials if you are already registered or enter different username if you are new user !"},status=status.HTTP_409_CONFLICT)

            this_user = User.objects.create_user(username=username,password=confirm_password,is_staff=0)
            this_user.save() 
            token = RefreshToken.for_user(this_user)
            referesh = str(token)
            access_token = str(token.access_token) 


            if   FCMDevice.objects.filter(registration_id=fcm_token).exists():

                #FCM Devices duplication handling start 
                if   FCMDevice.objects.filter(registration_id=fcm_token).filter(active=True).exists():
                    print("this device has duplicates this profile exist",fcm_token)
                    duplicates = FCMDevice.objects.filter(registration_id=fcm_token).filter(active=True)
                    for duplicate in duplicates:
                        print("duplicate user",duplicate.user_id)
                        duplicate.active = False
                        duplicate.save()

                #FCM Devices duplication handling end  

                fcm = FCMDevice(
                    registration_id=fcm_token, user_id=this_user.pk
                )
                fcm.save()
            else:
                fcm = FCMDevice(
                    registration_id=fcm_token, user_id=this_user.pk
                )
                fcm.save()

            
            data = {'userId': this_user.pk, 
                'access_token': access_token, 'refresh_token': referesh
            }


        return Response(data, status=status.HTTP_200_OK)
    

#Logout Api Class
class LogoutfromApp(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.method != 'POST':
            content = {'message': "Please Enter Post method"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        fcm_token = request.data.get('fcm_token') or None
        print("fcm tok",fcm_token)
        if fcm_token is None:
            content = {'message': "Please Enter User fcm_token"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        user_id = request.data.get('user_id') or None
        print("user_id  ",user_id)
        if user_id is None:
            content = {'message': "Please Enter User id"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST) 
        

        if not User.objects.filter(id=user_id).exists():
            content = {'message': "User does not exist"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        User_fcm_instance = FCMDevice.objects.filter(
            registration_id=fcm_token).filter(active=1).filter(user_id=user_id).first()
        print("User_fcm_instance  ",User_fcm_instance)
        if not User_fcm_instance:
            content = {'message': "User Device  does not exist"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            User_fcm_instance.active = False
            User_fcm_instance.save()

        if  Kitchen.objects.filter(approved_owner_id=user_id).filter(is_active=True).exists():
            Kitchen.objects.filter(approved_owner_id=user_id).filter(is_active=True).update(is_active=False)

        content = {'message': "Record Updated Succesfully"}
        return Response(content, status=status.HTTP_200_OK)
    


#Register  Rider
class  RegisterRider(APIView):
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.method != 'POST':
            content = {'message': "Please Enter Post method"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
 

        rider_email = request.data.get('rider_email') or None 
        if rider_email is None:
            content = {'message': "Please Enter rider email"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        if   RiderDetails.objects.filter(email=rider_email).exists():
            content = {'message': "Rider account with this email already exists"}
            return Response(content, status=status.HTTP_429_TOO_MANY_REQUESTS)

        rider_address = request.data.get('rider_address') or None 
        if rider_address is None:
            content = {'message': "Please Enter rider address"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        

        lat = None
        try:
            lat, long = OpenCage_for_address(rider_address)
        except: 
            print("400  4")
            data = {'message': 'This address cannot be traced please enter valid one  !'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)  
        
        
        if lat is None:
            print("400  5")
            data = {'message': 'This address cannot be located please enter valid one  !'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        rider_contact = request.data.get('rider_contact') or None
        # print("fcm tok",rider_contact)
        if rider_contact is None:
            content = {'message': "Please Enter rider contact"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        

        
        
        rider_name = request.data.get('rider_name') or None 
        if rider_name is None:
            content = {'message': "Please Enter rider name"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        spaces_info = check_spaces(rider_name) 
        if  spaces_info[0]  or  spaces_info[1]  or  spaces_info[2]:
            data = {'message': 'Space in rider name at start or end or in between characters is not allowed !'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
 

        fcm_token = request.data.get('fcm_token')
        print("rider fcm_token",fcm_token)   
        if fcm_token is None: 
            data = {'message':'Invalid Request, Missing FCM Token'}
            return Response(data,status=status.HTTP_409_CONFLICT)
        elif not fcm_token: 
            data = {'message':'Invalid Request,FCM Token is passed as an Empty string'}
            return Response(data,status=status.HTTP_409_CONFLICT)
        else:
            pass 


         
  
        if   RiderDetails.objects.filter(registration_id=fcm_token).exists():

            #FCM Devices duplication handling start 
            if   RiderDetails.objects.filter(registration_id=fcm_token).filter(device_active=True).exists():
                print("this device has duplicates this profile exist",fcm_token)
                duplicates = RiderDetails.objects.filter(registration_id=fcm_token).filter(device_active=True)
                for duplicate in duplicates:
                    print("duplicate user",duplicate.pk)
                    duplicate.device_active = False
                    duplicate.save()

            #FCM Devices duplication handling end  

            RiderDetails.objects.create(
                name = rider_name,
                address_details =  rider_address, 
                latitude =  lat,
                longitude = long,
                contact = rider_contact,
                email = rider_email,
                registration_id = fcm_token 
            )
        else:
            RiderDetails.objects.create(
                name = rider_name,
                address_details =  rider_address, 
                latitude =  lat,
                longitude = long,
                contact = rider_contact,
                email = rider_email,
                registration_id = fcm_token 
            )
        
 
        content = {'message': "Rider  registered  successfully !"}
        return Response(content, status=status.HTTP_200_OK)



#Get Rider Deatils 
class  GetRiderDeatils(APIView):
    def  get(self,request,email):
        if    RiderDetails.objects.filter(email=email).exists(): 
            return  Response(RiderDetailsSerializer(RiderDetails.objects.filter(email=email).first()).data, status=status.HTTP_200_OK)
        else:
            content = {'message': "Rider  deatils doesnot exist !"}
            return Response(content, status=status.HTTP_303_SEE_OTHER)
        

#Rider  Active/Inactive
class  SaveRideravailblity(APIView): 
    # permission_classes = (IsAuthenticated,)
    def  post(self, request):

        email = request.data.get('email') or None
        if email is None:
            print("400 av 1")
            data = {'message': 'Please Enter email'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        if  not  RiderDetails.objects.filter(email=email).exists():
            print("400 av  2")
            data = {'message': 'Rider  deatils doesnot exist'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        active_inactive = request.data.get('active_inactive')
        print("active_inactive",active_inactive)
        if active_inactive is None:
            print("400 av 3")
            data = {'message': 'Please Enter Rider availblity is True or False'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
         
        print("acttt",active_inactive,type(active_inactive))
        RiderDetails.objects.filter(email=email).update(is_active=active_inactive)

        data = {'message': 'Rider availblity updated successfully'}
        return Response(data, status=status.HTTP_200_OK)
    

#Get Rider Orders 
class  GetRiderOrders(APIView):
    def  get(self,request,email):
        if    RiderDetails.objects.filter(email=email).exists():
            today_Date = date.today()
            if     RiderOrders.objects.filter(rider_id__in=list(RiderDetails.objects.filter(email=email).values_list('pk',flat=True))).filter(is_delivered=False).filter(delivery_date=today_Date).exists(): 
                rider_orders_ordering = list(RiderOrders.objects.filter(rider_id__in=list(RiderDetails.objects.filter(email=email).values_list('pk',flat=True))).filter(is_delivered=False).filter(delivery_date=today_Date).order_by('-id').values_list('order_id',flat=True))
                preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(rider_orders_ordering)])
                return  Response(OrderSerializerforRider(Orders.objects.filter(pk__in=rider_orders_ordering).order_by(preserved),many=True).data, status=status.HTTP_200_OK)
            else:
                content = {'message': "Rider orders doesnot exist !"}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            content = {'message': "Rider doesnot exist !"}
            return Response(content, status=status.HTTP_303_SEE_OTHER)
        

#Get Rider Delivered Orders 
class  GetRiderDeliveredOrders(APIView):
    def  get(self,request,email):
        if    RiderDetails.objects.filter(email=email).exists():
            if     RiderOrders.objects.filter(rider_id__in=list(RiderDetails.objects.filter(email=email).values_list('pk',flat=True))).filter(is_delivered=True).exists(): 
                rider_orders_ordering = list(RiderOrders.objects.filter(rider_id__in=list(RiderDetails.objects.filter(email=email).values_list('pk',flat=True))).filter(is_delivered=True).order_by('-id').values_list('order_id',flat=True))
                preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(rider_orders_ordering)])
                return  Response(OrderDeliveredSerializerforRider(Orders.objects.filter(pk__in=rider_orders_ordering).order_by(preserved),many=True).data, status=status.HTTP_200_OK)
            else:
                content = {'message': "Rider Delivered orders doesnot exist !"}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            content = {'message': "Rider doesnot exist !"}
            return Response(content, status=status.HTTP_303_SEE_OTHER)

def check_spaces(s):
    has_space_start = s.startswith(' ')
    has_space_end = s.endswith(' ')
    has_space_between = ' ' in s.strip()  # Remove leading/trailing spaces for this check
    
    return has_space_start, has_space_end, has_space_between

 



# Register Customer
class RegisterCustomer(APIView): 
    def post(self, request):
        if request.method != 'POST':
            data = {'message': 'Please Enter Post method !'}
            return Response(data, status=status.HTTP_403_FORBIDDEN) 
        
        
        username = request.data.get('username') or None
        if username is None:
            data = {'message': 'Please Enter username'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        spaces_info = check_spaces(username) 
        if  spaces_info[0]  or  spaces_info[1]  or  spaces_info[2]:
            data = {'message': 'Space in username at start or end or in between characters is not allowed !'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


        if  User.objects.filter(username=username).exists():
            data = {'message': 'The username  is already taken'}
            return Response(data, status=status.HTTP_409_CONFLICT)


        email = request.data.get('email') or None
        if email is None:
            data = {'message': 'Please Enter email'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST) 

        

        password = request.data.get('password') or None
        if password is None:
            data = {'message': 'Please Enter password'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST) 
        

        fcm_token = request.data.get('fcm_token')
        print('fcm_token',fcm_token)   
        if fcm_token is None: 
            data = {'message':'Invalid Request, Missing FCM Token'}
            return Response(data,status=status.HTTP_409_CONFLICT)
        elif not fcm_token: 
            data = {'message':'Invalid Request,FCM Token is passed as an Empty string'}
            return Response(data,status=status.HTTP_409_CONFLICT)
        else:
            pass
        
         

 
 

        this_user = User.objects.create_user(username=username,email=email,password=password,is_staff=0)
        this_user.save()  


        if   FCMDevice.objects.filter(registration_id=fcm_token).exists():

            #FCM Devices duplication handling start 
            if   FCMDevice.objects.filter(registration_id=fcm_token).filter(active=True).exists():
                print("this device has duplicates this profile exist",fcm_token)
                duplicates = FCMDevice.objects.filter(registration_id=fcm_token).filter(active=True)
                for duplicate in duplicates:
                    print("duplicate user",duplicate.user_id)
                    duplicate.active = False
                    duplicate.save()

            #FCM Devices duplication handling end  

            fcm = FCMDevice(
                registration_id=fcm_token, user_id=this_user.pk
            )
            fcm.save()
        else:
            fcm = FCMDevice(
                registration_id=fcm_token, user_id=this_user.pk
            )
            fcm.save()

 
        
        data = {'userId': this_user.pk, 
            'username': username,
            'email': this_user.email  
        }


        return Response(data, status=status.HTTP_200_OK)
    


# Login Customer
class  LoginCustomer(APIView): 
    def post(self, request):
        if request.method != 'POST':
            data = {'message': 'Please Enter Post method !'}
            return Response(data, status=status.HTTP_403_FORBIDDEN) 
        
        
        username = request.data.get('username') or None
        if username is None:
            data = {'message': 'Please Enter username'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST) 

           

        password = request.data.get('password') or None
        if password is None:
            data = {'message': 'Please Enter password'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST) 
        

        user = authenticate(username=username,password=password)

        if  user is None:
            data = {'message': 'Username or password is incorrect'}
            return Response(data, status=status.HTTP_409_CONFLICT)


        fcm_token = request.data.get('fcm_token')
        print('fcm_token',fcm_token)   
        if fcm_token is None: 
            data = {'message':'Invalid Request, Missing FCM Token'}
            return Response(data,status=status.HTTP_409_CONFLICT)
        elif not fcm_token: 
            data = {'message':'Invalid Request,FCM Token is passed as an Empty string'}
            return Response(data,status=status.HTTP_409_CONFLICT)
        else:
            pass  


        user_pk = get_object_or_404(User.objects.only('pk'), username=username)


        if   FCMDevice.objects.filter(registration_id=fcm_token).exists():

            #FCM Devices duplication handling start 
            if   FCMDevice.objects.filter(registration_id=fcm_token).filter(active=True).exists():
                print("this device has duplicates this profile exist",fcm_token)
                duplicates = FCMDevice.objects.filter(registration_id=fcm_token).filter(active=True)
                for duplicate in duplicates:
                    print("duplicate user",duplicate.user_id)
                    duplicate.active = False
                    duplicate.save()

            #FCM Devices duplication handling end  

            fcm = FCMDevice(
                registration_id=fcm_token, user_id=user_pk.pk
            )
            fcm.save()
        else:
            fcm = FCMDevice(
                registration_id=fcm_token, user_id=user_pk.pk
            )
            fcm.save()
 
 
        data = {'userId': user_pk.pk, 
            'username': username,
            'email': user_pk.email 
        }


        return Response(data, status=status.HTTP_200_OK)
    

#Get Website Dynamics
class   GetWebsiteDynamics(APIView): 
    def  get(self,request): 
        return  Response(GetWebsiteDynamicsSerializer(WebsiteDynamic.objects.first()).data,
            status=status.HTTP_200_OK
        )
    

#Get Our Services
class   GetOurServices(APIView): 
    def  get(self,request): 
        return  Response(GetOurServicesSerializer(OurServicesSection.objects.first()).data,
            status=status.HTTP_200_OK
        )
    

#Get Our Clients
class   GetOurClients(APIView): 
    def  get(self,request): 
        return  Response(GetOurClientsSerializer(Clients.objects.first()).data,
            status=status.HTTP_200_OK
        )