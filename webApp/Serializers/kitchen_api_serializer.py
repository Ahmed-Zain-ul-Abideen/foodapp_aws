from rest_framework import serializers
from webApp.models import *
import json
from .Food_api_serializer import  menuorderaddsonSerializer,DailyMenuitemsSerializer,DealsSerializer,DailyMenuitemsSerializerformyorders,DealsSerializerformyorders
from datetime import date


class  AlladdsonSerializerhere(serializers.ModelSerializer):  
    class Meta:
        model = Alladdson 
        fields =  ('id','title','description','image','price','dicounted_price',)

class   UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email',)


class   KitchenAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = KitchenAddress
        fields = ('address_details',)


class   KitchenMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = KitchenMedia
        fields = ('file',)

class   KitchenSpecialitySerializer(serializers.ModelSerializer):
    kitchen_speciality_items = serializers.SerializerMethodField('kitchen_speciality_items_function')
    class Meta:
        model = KitchenSpeciality
        fields = ('kitchen_speciality_items',)

    def  kitchen_speciality_items_function(self, obj):
        items = json.decoder.JSONDecoder().decode(obj.items)
        if  not  len(items):
            return  None
        else:
            if  Menuitems.objects.filter(pk__in=items).exists(): 
                return   DailyMenuitemsSerializer(Menuitems.objects.filter(pk__in=items),many=True).data
            else:
                return   None



class  KitchenDeatilsSerializer(serializers.ModelSerializer): 
    # kitchen_admin = serializers.SerializerMethodField('kitchen_admin_function')
    kitchen_address_record = KitchenAddressSerializer()
    # kitchen_specialities = KitchenSpecialitySerializer()
    kitchen_media_records = KitchenMediaSerializer(many=True)
    class Meta:
        model = Kitchen
        fields = ('id','name','owner','contact','email','status','is_active','kitchen_address_record','kitchen_media_records',) 

    # def  kitchen_admin_function(self, obj):
    #     if  obj.kitchen_admin  is  None:
    #         return None
    #     else:
    #         return  UserSerializer(User.objects.filter(pk=obj.kitchen_admin).first()).data

class   ItemsorderaddsonSerializer(serializers.ModelSerializer):
    orderitems_addson = AlladdsonSerializerhere() 
    class Meta:
        model = Itemsorderaddson
        fields = ('orderitems_addson','quantity',) 

class   OrderItemsSerializer(serializers.ModelSerializer):
    item = DailyMenuitemsSerializerformyorders()
    orderitems_addson_records = ItemsorderaddsonSerializer(many=True)
    class Meta:
        model = OrderItems
        fields = ('item','orderitems_addson_records','extra_details','quantity','sub_total',) 



class   OrderAddsonSerializer(serializers.ModelSerializer):
    item = DailyMenuitemsSerializer()
    class Meta:
        model = OrderAddson
        fields = ('item','quantity',)

class  KitchenOrdersSerializer(serializers.ModelSerializer): 
    order_items = OrderItemsSerializer(many=True)
    order_addson = OrderAddsonSerializer(many=True)
    dropdown_statuses = serializers.SerializerMethodField('dropdown_statuses_function')
    class Meta:
        model = Orders
        fields = ('id','customer_name','user','total_price','status','order_items','order_addson','dropdown_statuses','created_at',)

    def   dropdown_statuses_function(self,obj): 
        return   OrderstatusSerializer(Orderstatus.objects.filter(role='Kitchen').exclude(status_title=obj.status).exclude(pk__in=list(OrderProcessedStatuses.objects.filter(order_id=obj.id).values_list('status_id',flat=True))).order_by('ordering_bit')[:1],many=True).data  
         

class  KitchenCookedOrdersSerializer(serializers.ModelSerializer): 
    order_items = OrderItemsSerializer(many=True)
    order_addson = OrderAddsonSerializer(many=True) 
    class Meta:
        model = Orders
        fields = ('id','customer_name','user','total_price','status','order_items','order_addson','created_at',)
      


class  OrderstatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orderstatus
        fields = ('id','status_title','is_pickup','is_in_process','its_color_code',)

class  OrdersSerializerForKitchenPayments(serializers.ModelSerializer): 
    # order_items = OrderItemsSerializer(many=True)
    # order_addson = OrderAddsonSerializer(many=True) 
    class Meta:
        model = Orders
        fields = ('id','total_price','status',)

class   kitchenOrdersPaymentSerializer(serializers.ModelSerializer):
    order =  OrdersSerializerForKitchenPayments()
    class Meta:
        model = kitchenOrdersPayment
        fields = ('kitchen_share_amount','status','order',)


class   RiderDeliveryPaymentSerializer(serializers.ModelSerializer):
    order =  OrdersSerializerForKitchenPayments()
    class Meta:
        model = RiderDeliveryPayment
        fields = ('rider_share_amount','status','order',)



class   KitchenPaymentsApiSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Paymentaccounts
        fields = ('iban_number','account_title','bank_name',)

class   SingleDailyOrderSerializer(serializers.ModelSerializer): 
    order_items = OrderItemsSerializer(many=True)
    order_addson = OrderAddsonSerializer(many=True) 
    class Meta:
        model = Orders
        fields = ('id','total_price','status','order_items','order_addson',)

# class  OrderMenuItemnewSerializer(serializers.ModelSerializer):
#     order_date = serializers.SerializerMethodField()
#     class Meta:
#         model = OrderMenuItems
#         fields = ('menu','extra_details','quantity','sub_total','order_date',)

#     def get_order_date(self, obj): 
#         return obj.order_date.date().strftime("%m/%d/%Y")


class  OrderMenufoodSerializer(serializers.ModelSerializer):
    item = DailyMenuitemsSerializerformyorders()
    class Meta:
        model = MenuFoodRecords
        fields = ('item','quantity','delivery_date',)

    # def get_order_date(self, obj): 
    #     return obj.order_date.date().strftime("%m/%d/%Y")

class    dealorderaddsonSerializer(serializers.ModelSerializer):
    orderdeal_addson = AlladdsonSerializerhere() 
    class Meta:
        model = Dealsorderaddson
        fields = ('orderdeal_addson','quantity',) 

class  OrderOrderDealItemsSerializer(serializers.ModelSerializer):
    deal = DealsSerializerformyorders()
    dealorder_addson_records = dealorderaddsonSerializer(many=True)
    class Meta:
        model = OrderDealItems
        fields = ('deal','dealorder_addson_records','extra_details','quantity','sub_total',)

class  OrderMenuItemforkitchenSerializer(serializers.ModelSerializer): 
    menuorder_addson_records = menuorderaddsonSerializer(many=True) 
    class Meta:
        model = OrderMenuItems
        fields = ('menuorder_addson_records',)

class  KitchenCurrentallOrdersSerializer(serializers.ModelSerializer): 
    order_items = OrderItemsSerializer(many=True)
    order_menu_food =  OrderMenufoodSerializer(many=True)
    order_deal_items = OrderOrderDealItemsSerializer(many=True)
    order_menu_items =  OrderMenuItemforkitchenSerializer(many=True)
    dropdown_statuses = serializers.SerializerMethodField('dropdown_statuses_function')
    class Meta:
        model = Orders
        fields = ('id','customer_name','user','total_price','status','its_color_code','order_deal_items','order_items','order_menu_food','order_menu_items','dropdown_statuses','created_at','has_menu',)

    def   dropdown_statuses_function(self,obj): 
        today = date.today()
        return   OrderstatusSerializer(Orderstatus.objects.filter(role='Kitchen').exclude(status_title=obj.status).exclude(pk__in=list(OrderProcessedStatuses.objects.filter(order_id=obj.id).filter(processed_date=today).values_list('status_id',flat=True))).order_by('ordering_bit')[:1],many=True).data

    def to_representation(self, instance):
        # Filter the related B records by today's date
        today = date.today()

        # Use the serializer to filter and represent the related records
        order_menu_food_filtered = instance.order_menu_food.filter(delivery_date=today)
        order_items_filtered = instance.order_items.filter(delivery_date=today)
        order_deal_items_filtered = instance.order_deal_items.filter(delivery_date=today)

        # Now, use the filtered querysets in the response
        representation = super().to_representation(instance)

        # Replace the fields with the filtered results
        representation['order_menu_food'] = OrderMenufoodSerializer(order_menu_food_filtered, many=True).data
        representation['order_items'] = OrderItemsSerializer(order_items_filtered, many=True).data
        representation['order_deal_items'] = OrderOrderDealItemsSerializer(order_deal_items_filtered, many=True).data

        return representation
    


class  KitchenallcookedOrdersSerializer(serializers.ModelSerializer): 
    order_items = OrderItemsSerializer(many=True)
    order_menu_food =  OrderMenufoodSerializer(many=True)
    order_deal_items = OrderOrderDealItemsSerializer(many=True) 
    class Meta:
        model = Orders
        fields = ('id','customer_name','user','total_price','status','its_color_code','order_deal_items','order_items','order_menu_food','created_at','has_menu',)

 

    def to_representation(self, instance):
        # Filter the related B records by today's date
         

        # Use the serializer to filter and represent the related records
        order_menu_food_filtered = instance.order_menu_food.filter(is_cooked=True).order_by('delivery_date')
        order_items_filtered = instance.order_items.filter(is_cooked=True)
        order_deal_items_filtered = instance.order_deal_items.filter(is_cooked=True)

        # Now, use the filtered querysets in the response
        representation = super().to_representation(instance)

        # Replace the fields with the filtered results
        representation['order_menu_food'] = OrderMenufoodSerializer(order_menu_food_filtered, many=True).data
        representation['order_items'] = OrderItemsSerializer(order_items_filtered, many=True).data
        representation['order_deal_items'] = OrderOrderDealItemsSerializer(order_deal_items_filtered, many=True).data

        return representation