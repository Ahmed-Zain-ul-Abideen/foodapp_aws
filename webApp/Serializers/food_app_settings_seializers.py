from rest_framework import serializers
from webApp.models import * 


class  GetPaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paymentaccounts
        fields = ('iban_number','account_title',)


class  FoodappSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodappSettings
        fields = ('contact','terms_and_c',)


class  GetPaymentSettingsSerializer(serializers.Serializer):
    data = serializers.SerializerMethodField()
    
    def get_data(self, obj):
        print("cus obj",obj)
        data_obj = {}
        admins = list(User.objects.filter(is_superuser=True).values_list('pk',flat=True))
        if  not  Paymentaccounts.objects.filter(user_id__in=admins).exists():
            data_obj['payment_accounts'] = []
        else:
            data_obj['payment_accounts'] = GetPaymentsSerializer(Paymentaccounts.objects.filter(user_id__in=admins),many=True).data

        if   FoodappSettings.objects.exists():
            setting_serialized = FoodappSettingsSerializer(FoodappSettings.objects.last()).data
            data_obj['contact']   =  setting_serialized.get('contact')
            data_obj['t_n_c']   = setting_serialized.get('terms_and_c')
        else:
            data_obj['contact'] = None
            data_obj['t_n_c'] =  None

        return data_obj



# class  GetPaymentSettingsSerializerold(serializers.ModelSerializer):
#     payment_accounts = serializers.SerializerMethodField('get_data')
#     class Meta:
#         model = FoodappSettings
#         fields = ('payment_accounts','contact')


#     def  get_data(self,instance):
#         print("in get data")
#         admins = list(User.objects.filter(is_superuser=True).values_list('pk',flat=True))
#         return GetPaymentsSerializer(Paymentaccounts.objects.filter(user_id__in=admins),many=True).data

    
#     def to_representation(self, instance):
#         # Check if the instance is a queryset and if it's empty
#         if isinstance(instance, list) and not instance:
#             admins = list(User.objects.filter(is_superuser=True).values_list('pk',flat=True))
#             if  not  Paymentaccounts.objects.filter(user_id__in=admins).exists(): 
#                 print("not instance  and no paym acc")
#                 return {'contact': None,'payment_accounts':[]}
            
#             print("not instance  and  paym acc")
#             return {'contact': None,'payment_accounts': GetPaymentsSerializer(Paymentaccounts.objects.filter(user_id__in=admins),many=True).data}

#         # Call the super method to get the default representation
#         representation = super().to_representation(instance)

#         # If the instance is a single object, ensure it gets properly handled
#         if isinstance(instance, dict):
#             print("yes instance")
#             return representation
        
#         # Handle any other cases as needed
#         print("reurned outside")
#         return representation
