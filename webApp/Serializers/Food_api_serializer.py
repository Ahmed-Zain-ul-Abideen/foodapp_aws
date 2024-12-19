from rest_framework import serializers
from webApp.models import *
import json

class  AlladdsonSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Alladdson 
        fields =  ('id','title','description','image','price','dicounted_price',)

class  DailyMenuitemsSerializer(serializers.ModelSerializer):
    item_addson_records = AlladdsonSerializer(many=True, read_only=True) 
    class Meta:
        model = Menuitems 
        fields =  ('id','title','description','image','price','dicounted_price','exclusive','dicounted_price','item_addson_records',)

class  DailyMenuitemsSerializerformyorders(serializers.ModelSerializer): 
    class Meta:
        model = Menuitems 
        fields =  ('id','title','description','image','price','dicounted_price','exclusive','dicounted_price',)

class  MenuSerializer(serializers.ModelSerializer): 
    associated_items = serializers.SerializerMethodField()
    menu_addson_records = AlladdsonSerializer(many=True, read_only=True) 
    class Meta:
        model = Menu 
        fields =  ('id','total_price','dicounted_price','title','description','associated_items','menu_addson_records',)

    def get_associated_items(self,obj):
        items_list = json.decoder.JSONDecoder().decode(obj.associated_items)
        return_data = []
        for  k,v in items_list.items():
            # print("k,v",k,v)
            # key_var = "day_"+ str(k)
            # del items_list[str(k)]
            if  v ==  "None": 
                return_data.append(None)
                # return_data[key_var] = "N/A"
            else:
                return_data.append(DailyMenuitemsSerializer(Menuitems.objects.filter(pk=int(v)).first()).data)
                # return_data[key_var] = DailyMenuitemsSerializer(Menuitems.objects.filter(pk=int(v)).first()).data
        return return_data
        return  DailyMenuitemsSerializer(Menuitems.objects.filter(pk__in= [value for value in items.values() if value is not None]),many=True).data



class  MenuSerializerformyorders(serializers.ModelSerializer):   
    class Meta:
        model = Menu 
        fields =  ('id','total_price','dicounted_price','title','description',) 


class   menuorderaddsonSerializer(serializers.ModelSerializer):
    ordermenu_addson = AlladdsonSerializer() 
    class Meta:
        model = Menuorderaddson
        fields = ('ordermenu_addson','quantity',) 


class  OrderMenuItemSerializer(serializers.ModelSerializer):
    menu = MenuSerializerformyorders()
    menuorder_addson_records = menuorderaddsonSerializer(many=True)
    order_date = serializers.SerializerMethodField()
    class Meta:
        model = OrderMenuItems
        fields = ('menu','menuorder_addson_records','extra_details','quantity','sub_total','order_date',)

    def get_order_date(self, obj): 
        return obj.order_date.date().strftime("%m/%d/%Y")

class  MenuOrdersSerializer(serializers.ModelSerializer):
    order_menu_items = OrderMenuItemSerializer(many=True)
    class Meta:
        model = Orders
        fields = ('id','customer_name','user','order_menu_items','total_price','status','created_at',)


class  MenuCategorysSerializer(serializers.ModelSerializer): 
    menu_categories =  MenuSerializer(many=True)
    class Meta:
        model = MenuCategory 
        fields =  ('id','title','menu_categories',)

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance) 
    #     if  not  instance.menu_categories.exists():
    #         pass
    #         # print("isntgff",instance.title)
    #         # return None  # Exclude this instance from serialization output
    #     else:
    #         print("bemaak",instance.title)
    #         return representation



class  SingleitemsSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Menuitems 
        fields =  ('id','title','description','image','price',)


class DealsSerializer(serializers.ModelSerializer):
    deal_items = DailyMenuitemsSerializer(many=True, read_only=True)
    deal_addson_records = AlladdsonSerializer(many=True, read_only=True) 
    class Meta:
        model = Deals
        fields =  ('id','title','file','price','description','deal_items','deal_addson_records',)  


class DealsSerializerformyorders(serializers.ModelSerializer):
    deal_items = DailyMenuitemsSerializer(many=True, read_only=True)  
    class Meta:
        model = Deals
        fields =  ('id','title','file','price','description','deal_items',) 