from rest_framework import serializers
from webApp.models import *
from  webApp.Serializers.kitchen_api_serializer  import  *
from  webApp.Serializers.Food_api_serializer  import  *
from datetime import date

class  RiderDetailsSerializer(serializers.ModelSerializer): 
    class Meta:
        model = RiderDetails 
        fields =   '__all__'


class  KitchenDeatilsSerializerForRider(serializers.ModelSerializer):  
    kitchen_address_record = KitchenAddressSerializer()  
    class Meta:
        model = Kitchen
        fields = ('name','owner','contact','kitchen_address_record',) 


class  OrderstatusSerializerforRider(serializers.ModelSerializer):
    class Meta:
        model = Orderstatus
        fields = ('id','status_title','is_delivered','is_rider_on_way',)

class  OrderSerializerforRider(serializers.ModelSerializer):
    # order_items = OrderItemsSerializer(many=True)
    # order_menu_items = OrderMenuItemSerializer(many=True)
    kitchen = KitchenDeatilsSerializerForRider()
    dropdown_statuses = serializers.SerializerMethodField('dropdown_statuses_function')
    class Meta:
        model = Orders 
        fields =    ('id','customer_name','contact','address_details','is_cod','has_menu','total_price','status','dropdown_statuses','kitchen',)

    def   dropdown_statuses_function(self,obj):
        today = date.today() 
        return   OrderstatusSerializerforRider(Orderstatus.objects.filter(role='Rider').exclude(status_title=obj.status).exclude(pk__in=list(OrderProcessedStatuses.objects.filter(order_id=obj.id).filter(processed_date=today).values_list('status_id',flat=True))).order_by('ordering_bit')[:1],many=True).data 
    


class  OrderDeliveredSerializerforRider(serializers.ModelSerializer):
    # order_items = OrderItemsSerializer(many=True)
    # order_menu_items = OrderMenuItemSerializer(many=True)
    kitchen = KitchenDeatilsSerializerForRider() 
    class Meta:
        model = Orders 
        fields =    ('id','customer_name','contact','address_details','is_cod','total_price','status','kitchen',)
 

 

class  GetWebsiteDynamicsSerializer(serializers.ModelSerializer):  
    class Meta:
        model = WebsiteDynamic 
        fields =  '__all__'


class  AllServicesSerializer(serializers.ModelSerializer):   
    class Meta:
        model = OurServices 
        fields =    ("title","description","image",)


class  AllClientsSerializer(serializers.ModelSerializer):   
    class Meta:
        model = OurClients 
        fields =    ("client","name","review","avatar",)

class  GetOurServicesSerializer(serializers.ModelSerializer):  
    all_services = AllServicesSerializer(many=True)
    class Meta:
        model = OurServicesSection 
        fields =  ('title','all_services',)


class  GetOurClientsSerializer(serializers.ModelSerializer):  
    all_clients = AllClientsSerializer(many=True)
    class Meta:
        model = Clients 
        fields =  ('title','all_clients',)



class  MyallordersSerializer(serializers.ModelSerializer): 
    order_items = OrderItemsSerializer(many=True)
    order_addson = OrderAddsonSerializer(many=True)
    order_menu_items =  OrderMenuItemSerializer(many=True)
    order_deal_items = OrderOrderDealItemsSerializer(many=True)
    class Meta:
        model = Orders
        fields = ('id','customer_name','user','total_price','status','its_color_code','has_menu','order_deal_items','order_addson','order_items','order_menu_items','created_at',)