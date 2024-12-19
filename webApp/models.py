from django.db import models
from django.contrib.auth.models import User,Permission,Group
from django_resized import ResizedImageField
from django.core.validators import MinValueValidator, MaxValueValidator

#Deals(offers)
class  Deals(models.Model): 
    title =  models.CharField(max_length=522)
    file = ResizedImageField(size=None,null=True, blank=True,upload_to="static/Deals_avatars")
    price = models.DecimalField(max_digits=15,decimal_places=2,null=True)
    description = models.TextField(null=True)

#Kitchen
class Kitchen(models.Model):
    name = models.CharField(max_length=522) 
    owner = models.CharField(max_length=522) 
    approved_owner = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    kitchen_admin = models.PositiveIntegerField(null=True)
    contact =  models.CharField(max_length=522)
    email = models.EmailField()
    status = models.CharField(max_length=522,default="pending")
    is_active = models.BooleanField(default=True)


#KitchenSpeciality
class KitchenSpeciality(models.Model):
    Kitchen = models.OneToOneField(Kitchen,related_name="kitchen_specialities", on_delete=models.CASCADE, null=True)
    items = models.TextField(default="[]")


#KitchenAddress
class KitchenAddress(models.Model):
    Kitchen = models.OneToOneField(Kitchen,related_name='kitchen_address_record', on_delete=models.CASCADE, null=True)
    address_line1 = models.CharField(max_length=122,null=True)
    address_line2 = models.CharField(max_length=122,null=True)
    city = models.CharField(max_length=122,null=True)
    country = models.CharField(max_length=122,null=True)
    postal_code = models.CharField(max_length=122,null=True) 
    address_details = models.CharField(max_length=522,null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)


#KitchenMedia
class KitchenMedia(models.Model):
    Kitchen = models.ForeignKey(Kitchen,related_name="kitchen_media_records", on_delete=models.CASCADE, null=True)
    file = ResizedImageField(size=None,null=True, blank=True,upload_to="static/kitchen_media")



#AdminAddress
class  AdminAddress(models.Model):
    admin_address = models.OneToOneField(User,related_name='admin_adrress_record', on_delete=models.CASCADE, null=True)
    address_details = models.CharField(max_length=522,null=True)
    address_line1 = models.CharField(max_length=122,null=True)
    address_line2 = models.CharField(max_length=122,null=True)
    city = models.CharField(max_length=122,null=True)
    country = models.CharField(max_length=122,null=True)
    postal_code = models.CharField(max_length=122,null=True) 
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)


#MenuCategory
class MenuCategory(models.Model):
    title = models.CharField(max_length=522)
    menu_count = models.PositiveIntegerField(default=1)
    Kitchen_share_percent =  models.CharField(max_length=522,null=True)



#Menu
class Menu(models.Model):
    title = models.CharField(max_length=522)
    description = models.TextField()
    category = models.ForeignKey(MenuCategory,related_name="menu_categories", on_delete=models.CASCADE, default='') 
    associated_items = models.TextField(null=True)
    total_price = models.DecimalField(max_digits=15,decimal_places=2,null=True)
    dicounted_price = models.DecimalField(max_digits=15,decimal_places=2,null=True) 



#Menudivison
class Menudivison(models.Model):
    title = models.CharField(max_length=522) 
    menu = models.ForeignKey(Menu,related_name="menu_divisions", on_delete=models.CASCADE, default='')



#Menusubdivison
class Menusubdivison(models.Model):
    title = models.CharField(max_length=522) 
    menudiv = models.ForeignKey(Menudivison,related_name="menu_sub_divisions", on_delete=models.CASCADE, default='')


#Menuitems
class Menuitems(models.Model):
    title = models.CharField(max_length=522)
    description = models.TextField()
    image = models.FileField(max_length=122,null=True, blank=True,upload_to="static/items_avatar")
    price = models.DecimalField(max_digits=15,decimal_places=2,null=True) 
    daily_deals = models.BooleanField(default=True)
    ads_on = models.BooleanField(default=False)
    exclusive = models.BooleanField(default=False)
    dicounted_price = models.DecimalField(max_digits=15,decimal_places=2,null=True)
    deal = models.ManyToManyField(Deals,related_name="deal_items")


#Payment Methods
class PaymentMethods(models.Model):  
    user = models.ForeignKey(User,related_name='PaymentMethod', on_delete=models.CASCADE, default='') 
    brand = models.CharField(max_length=122,null=True)
    card_id = models.CharField(max_length=122,null=True)
    ccv = models.IntegerField(null=True)
    exp_month = models.CharField(max_length=122,null=True)
    exp_year = models.CharField(max_length=122,null=True)
    last4 = models.CharField(max_length=122,null=True)
    name_on_card = models.CharField(max_length=122,null=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add = True,null=True)
    updated_at = models.DateTimeField(auto_now_add = True,null=True) 

    def __str__(self):
        return str(self.user.username)

#Orders
class Orders(models.Model):
    user = models.CharField(max_length=522,null=True)
    customer_name = models.CharField(max_length=522,null=True)
    order_fcm = models.TextField(null=True)
    total_price = models.DecimalField(max_digits=15,decimal_places=2,null=True) 
    payment_method = models.ForeignKey(PaymentMethods, on_delete=models.CASCADE, null=True)
    is_cod = models.BooleanField(null=True)
    status = models.CharField(max_length=222,default='pending')
    kitchen = models.ForeignKey(Kitchen,related_name='Kitchen_Orders', on_delete=models.CASCADE, null=True)
    address_details = models.CharField(max_length=522,null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    contact =  models.CharField(max_length=522,null=True)
    rider_pending = models.BooleanField(default=False)
    subscription_info = models.JSONField(null=True)
    extra_notes =  models.TextField(null=True)
    order_details =  models.TextField(null=True)
    to_be_confirmed = models.BooleanField(default=True)
    is_cancelled = models.BooleanField(default=False)
    kitchen_pickup_date = models.DateField(auto_now_add=True,null=True)
    is_delivered = models.BooleanField(default=False)
    has_menu = models.BooleanField(default=False)
    max_deliverable = models.PositiveIntegerField(default=1)
    last_date_to_deliver =  models.DateField(null=True)
    kitchen_to_customer_distance = models.DecimalField(max_digits=15,decimal_places=2,null=True)
    its_color_code = models.CharField(max_length=522,null=True)
    created_at = models.DateTimeField(auto_now_add = True,null=True)
    updated_at = models.DateTimeField(auto_now_add = True,null=True)

    def __str__(self):
        return str(self.user)
    

#Order Items
class OrderItems(models.Model):
    order = models.ForeignKey(Orders,related_name='order_items', on_delete=models.CASCADE, default='')
    item = models.ForeignKey(Menuitems,related_name='item_ordered', on_delete=models.CASCADE, default='')
    extra_details = models.CharField(max_length=500,null=True)  
    quantity = models.IntegerField(null=True)
    sub_total = models.DecimalField(max_digits=15,decimal_places=2,null=True)
    delivery_date = models.DateField(auto_now_add = True,null=True)
    is_cooked = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add = True,null=True)
    updated_at = models.DateTimeField(auto_now_add = True,null=True)

    def __str__(self):
        return str(self.item.title)
    

#Order Menu Items
class OrderMenuItems(models.Model):
    order = models.ForeignKey(Orders,related_name='order_menu_items', on_delete=models.CASCADE, default='')
    menu = models.ForeignKey(Menu,related_name='menu_ordered', on_delete=models.CASCADE, default='')
    extra_details = models.CharField(max_length=500,null=True)  
    quantity = models.IntegerField(null=True)
    sub_total = models.DecimalField(max_digits=15,decimal_places=2,null=True) 
    order_date = models.DateTimeField(auto_now_add = True,null=True)
    updated_at = models.DateTimeField(auto_now_add = True,null=True)

    def __str__(self):
        return str(self.menu.title)
    

#Order Addson
class OrderAddson(models.Model): 
    order = models.ForeignKey(Orders,related_name='order_addson', on_delete=models.CASCADE, default='')
    item = models.ForeignKey(Menuitems,related_name='adds_on_items', on_delete=models.CASCADE, default='')
    quantity = models.PositiveIntegerField(null=True)



# #Kitchen  Orders
# class KitchenOrders(models.Model): 
#     order = models.ForeignKey(Orders,related_name='Order_Orders', on_delete=models.CASCADE, null=True)
#     kitchen = models.ForeignKey(Orders,related_name='Kitchen_Orders', on_delete=models.CASCADE, null=True)

class LinkGroupModule(models.Model):
    group = models.CharField(max_length=522,null=True)
    module = models.CharField(max_length=522,null=True)

# SystemModules
class SystemModules(models.Model):
    module = models.CharField(max_length=522,null=True)


#Payment Accounts
class  Paymentaccounts(models.Model):
    user = models.ForeignKey(User,related_name='user_payment_accounts', on_delete=models.CASCADE, null=True)
    iban_number = models.CharField(max_length=522,null=True)
    account_title = models.CharField(max_length=522,null=True) 
    bank_name = models.CharField(max_length=522,null=True)


#Food app Settings
class  FoodappSettings(models.Model):
    contact =  models.CharField(max_length=522,null=True)
    orders_radius = models.PositiveIntegerField(default=50)
    terms_and_c = models.TextField(null=True)
    Kitchen_share_percent = models.PositiveIntegerField(
        default=90,
        validators=[
            MinValueValidator(50),  # Ensures the value is >= 50
            MaxValueValidator(100)   # Ensures the value is <= 100
        ]
    )

class  Orderstatus(models.Model):
    status_title =  models.CharField(max_length=522,null=True)
    role = models.CharField(max_length=522,null=True)
    is_pickup = models.BooleanField(default=False)
    ordering_bit = models.PositiveIntegerField(default=0)
    is_delivered = models.BooleanField(default=False)
    is_in_process = models.BooleanField(default=False)
    is_rider_on_way = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    is_pending = models.BooleanField(default=False)
    is_cod = models.BooleanField(default=False)
    its_color_code = models.CharField(max_length=522,null=True)

# kitchen Order Payment Share
class kitchenOrdersPayment(models.Model):
    Kitchen = models.ForeignKey(Kitchen,related_name="kitchen_payment_info", on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Orders,related_name='order_payment_info', on_delete=models.CASCADE, default='')
    kitchen_share_amount = models.DecimalField(max_digits=15,decimal_places=2,null=True)
    status = models.CharField(max_length=522,default='pending')
    is_payable = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    delivery_date = models.DateField(auto_now_add = True,null=True)



#RiderDetails
class  RiderDetails(models.Model): 
    name = models.CharField(max_length=522)
    address_details = models.CharField(max_length=522,null=True)
    address_line1 = models.CharField(max_length=122,null=True)
    address_line2 = models.CharField(max_length=122,null=True)
    city = models.CharField(max_length=122,null=True)
    country = models.CharField(max_length=122,null=True)
    postal_code = models.CharField(max_length=122,null=True) 
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    contact = models.CharField(max_length=522)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    registration_id	= models.TextField(null=True)
    device_active = models.BooleanField(default=True)


#RiderOrders
class  RiderOrders(models.Model):
    rider =  models.ForeignKey(RiderDetails,related_name="rider_orders", on_delete=models.CASCADE, null=True)
    order =  models.ForeignKey(Orders,related_name="order_delivery", on_delete=models.CASCADE, null=True)
    is_delivered = models.BooleanField(default=False)
    delivery_distance = models.DecimalField(max_digits=15,decimal_places=2,null=True)
    delivery_date = models.DateField(auto_now_add = True,null=True)


#OrderProcessedStatuses
class  OrderProcessedStatuses(models.Model):
    status_id =  models.PositiveIntegerField()
    order_id =  models.PositiveIntegerField()
    processed_date = models.DateField(auto_now_add=True,null=True)


#WebsiteDynamic
class  WebsiteDynamic(models.Model):
    Hero_section_title = models.CharField(max_length=522)
    Hero_section_description = models.TextField()
    Hero_section_image = models.FileField(max_length=522,null=True, blank=True,upload_to="static/website_dynamics")
    about_section_title = models.CharField(max_length=522)
    about_section_description = models.TextField()
    about_section_image = models.FileField(max_length=522,null=True, blank=True,upload_to="static/website_dynamics")
    daily_section_title = models.CharField(max_length=522)
    daily_section_description = models.TextField()
    menus_section_title = models.CharField(max_length=522)
    menus_section_description = models.TextField()


#OurServicesSection
class  OurServicesSection(models.Model):
    title = models.CharField(max_length=522)


#OurServices
class  OurServices(models.Model):
    title = models.CharField(max_length=522)
    description = models.TextField()
    image = models.FileField(max_length=522,null=True, blank=True,upload_to="static/our_services")
    service = models.ForeignKey(OurServicesSection,related_name="all_services", on_delete=models.CASCADE, null=True)


#Rider Payment Accounts
class   RiderPaymentaccounts(models.Model):
    rider = models.ForeignKey(RiderDetails,related_name='rider_payment_accounts', on_delete=models.CASCADE, null=True)
    iban_number = models.CharField(max_length=522,null=True)
    account_title = models.CharField(max_length=522,null=True) 
    bank_name = models.CharField(max_length=522,null=True)



#Rider Delivery Payment Share
class  RiderDeliveryPayment(models.Model):
    rider = models.ForeignKey(RiderDetails,related_name="rider_delivery_payment", on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Orders,related_name='order_delivery_info', on_delete=models.CASCADE, default='')
    rider_share_amount = models.DecimalField(max_digits=15,decimal_places=2,null=True)
    status = models.CharField(max_length=522,default='pending')
    is_payable = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    delivery_date = models.DateField(auto_now_add = True,null=True)


#Clients
class   Clients(models.Model):
    title = models.CharField(max_length=522)
    description = models.TextField(null=True)

#Our Clients
class   OurClients(models.Model):
    client = models.ForeignKey(Clients,related_name='all_clients', on_delete=models.CASCADE)
    name = models.CharField(max_length=522) 
    review = models.TextField() 
    avatar = ResizedImageField(size=None,null=True, blank=True,upload_to="static/clients_avatar")



#Menu Food Records
class  MenuFoodRecords(models.Model):
    order = models.ForeignKey(Orders,related_name='order_menu_food', on_delete=models.CASCADE, default='')
    menu = models.ForeignKey(Menu,related_name='menu_related_food', on_delete=models.CASCADE, default='')
    item = models.ForeignKey(Menuitems,related_name='menu_order_item', on_delete=models.CASCADE, default='')
    quantity = models.IntegerField(null=True)
    delivery_date = models.DateField()
    is_cooked = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)


#Rider Comission settings
class  RiderComissionsettings(models.Model):
    by_distance = models.PositiveIntegerField(default=1)
    amount_share = models.PositiveIntegerField(default=100)

#NewsletterRecords
class  NewsletterRecords(models.Model): 
    email = models.EmailField()
    

#Order Deal Items
class OrderDealItems(models.Model):
    order = models.ForeignKey(Orders,related_name='order_deal_items', on_delete=models.CASCADE, default='')
    deal = models.ForeignKey(Deals,related_name='deal_ordered', on_delete=models.CASCADE, default='')
    extra_details = models.CharField(max_length=500,null=True)  
    quantity = models.IntegerField(null=True)
    sub_total = models.DecimalField(max_digits=15,decimal_places=2,null=True) 
    delivery_date = models.DateField(auto_now_add = True,null=True)
    updated_at = models.DateTimeField(auto_now_add = True,null=True)
    is_cooked = models.BooleanField(default=False)

    def __str__(self):
        return str(self.deal.title)
    


#Alladdson
class  Alladdson(models.Model):
    deal = models.ManyToManyField(Deals,related_name="deal_addson_records")
    item = models.ManyToManyField(Menuitems,related_name="item_addson_records")
    menu = models.ManyToManyField(Menu,related_name="menu_addson_records")
    title = models.CharField(max_length=522)
    description = models.TextField()
    image = models.FileField(max_length=122,null=True, blank=True,upload_to="static/all_addson")
    price = models.DecimalField(max_digits=15,decimal_places=2,null=True)
    dicounted_price = models.DecimalField(max_digits=15,decimal_places=2,null=True)



#Itemsorderaddson
class  Itemsorderaddson(models.Model):
    order_item = models.ForeignKey(OrderItems,related_name="orderitems_addson_records",on_delete=models.CASCADE,null=True)
    orderitems_addson = models.ForeignKey(Alladdson,related_name="the_itemorder_addson",on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField(null=True)


#Dealsorderaddson
class  Dealsorderaddson(models.Model):
    dealorder_item = models.ForeignKey(OrderDealItems,related_name="dealorder_addson_records",on_delete=models.CASCADE,null=True)
    orderdeal_addson = models.ForeignKey(Alladdson,related_name="the_dealorder_addson",on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField(null=True)


#Menuorderaddson
class  Menuorderaddson(models.Model):
    menuorder_item = models.ForeignKey(OrderMenuItems,related_name="menuorder_addson_records",on_delete=models.CASCADE,null=True)
    ordermenu_addson = models.ForeignKey(Alladdson,related_name="the_menuorder_addson",on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField(null=True)
     