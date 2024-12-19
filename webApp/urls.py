from django.urls import path 
from  webApp.views.Home import Index
from webApp.views.dashboard import authview, dashboardkitchenview, dashboardgroupview, dashboarduserview, dashboardmenuview, dashboardsystemmodulesview, dashboardordersview, dashboardpaymentaccountview, dashboardorderstatusview,dashboardserviceview,dashboardclientsview,dashboardriderview,dashboardoffersview,dashboardaddonsview
from webApp.views.Others.menus_view import *
from webApp.views.Users.usersview import *
from django.contrib.auth import views as auth_views
from webApp.views.Api_s_views import Users_apis_view
from webApp.views.Api_s_views.Food_apis_view  import  *
from webApp.views.Api_s_views.Kitchen_apis_view  import  *
from webApp.views.expo_notif_view import *

#JWT 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    # Push Notification URL

    path('send-push', send_notification_view, name='send_push'),

    # Data Notification URL

    path('send-data-notif', send_data_notification_view, name='send_data_notif'),



    path('demo',Home,name='demo'), 
    path('', sign_in, name='sign_in'),
    # path('', auth_receiver, name='login'),
    path('logout', sign_out, name='logout'),
    # path('login', auth_receiver, name='login'),
    path('auth-r', auth_receiver, name='login'),
    path("sign_out/", auth_views.LogoutView.as_view(), name="sign_out"),

    path('soc_logi', socback_log_redirect, name='soc_logi'),
    path('lnkd_logi', lnkd_log_redirect, name='lnkd_logi'),
    # path('login', sign_in, name='sign_in'),
    # path('bb',Homecf,name='demob'),
    # path('bb',Homec,name='demobae'),
    # path('sug',Users_Suggestions,name='sug'),

    # Delete Quiz 
    # path('delete_quiz_view',  DeleteQuiz  , name="delete_quiz_view"),

    # Index page
    path('index', Index , name='index'), 

    # Login Page
    path('login', authview.LoginForm.as_view(), name="login-dashboard"),
    path('user-login', authview.UserLogin,name="user-login"),
    path('user_logout', authview.UserLogOut,name="user_logout"),
    path('permission_denied', authview.permissionview ,name="permission_denied"),

    # Kitchen
    path('add_kitchen_form/<int:add_button_clicked>', dashboardkitchenview.AddKitchenForm , name='add_kitchen_form'), 
    path('add_kitchen', dashboardkitchenview.AddKitchen , name='add_kitchen'),
    path('kitchens', dashboardkitchenview.Kitchenlist , name="kitchens"), 
    path('delete_kitchen', dashboardkitchenview.DeleteKitchen , name="delete_kitchen"),
    path('edit_kitchen_form/<int:id>/<int:add_button_clicked>', dashboardkitchenview.EditKitchenForm , name='edit_kitchen_form'), 
    path('edit_kitchen', dashboardkitchenview.EditKitchen , name='edit_kitchen'), 
    path('kitchen_table_custom_search', dashboardkitchenview.KitchenCustomSearch , name="kitchen_table_custom_search"), 
    path('select_kitchen_specialities', dashboardkitchenview.SelectKitchenSpecialities , name='select_kitchen_specialities'),
    path('save_kitchen_speciality', dashboardkitchenview.SaveKitchenSpeciality , name='save_kitchen_speciality'),
    path('upd_kitchen_status', dashboardkitchenview.UpdateKitchenStatus , name='upd_kitchen_status'),
    path('selected_items/<int:id>', dashboardkitchenview.KitchenSpecialitylist , name='selected_items'),
    path('kitchen_orders_list/<int:id>', dashboardkitchenview.KitchenOrderslist , name='kitchen_orders_list'), 
    path('save_kitchen_isactive', dashboardkitchenview.SaveKitchenisactive , name='save_kitchen_isactive'),
    path('my_kitchen_orders', dashboardkitchenview.MyKitchenOrdersList , name='my_kitchen_orders'),
    path('my_kitchen_previous_orders/<int:id>', dashboardkitchenview.KitchenPreviousOrderslist , name='my_kitchen_previous_orders'),


    # Group 
    path('groups', dashboardgroupview.Grouplist , name="groups"),
    path('add_group_form/<int:add_button_clicked>', dashboardgroupview.AddGroupForm , name='add_group_form'), 
    path('add_group', dashboardgroupview.AddGroup , name='add_group'),
    path('edit_user_role', dashboardgroupview.EditUserRole , name='edit_user_role'),
    path('edit_user_role_notif', dashboardgroupview.EditUserRoleNotif , name='edit_user_role_notif'),
    path('edit_role_permissions/<int:id>/<int:add_button_clicked>', dashboardgroupview.EditRolePermissions , name='edit_role_permissions'),
    path('submit_edit_role_permissions', dashboardgroupview.SubmitEditRolePermissions , name='submit_edit_role_permissions'),
    path('delete_role', dashboardgroupview.DeleteGroup , name="delete_role"),
    path('role_table_custom_search', dashboardgroupview.RolesCustomSearch , name="role_table_custom_search"), 



    # Users
    path('users', dashboarduserview.Userlist , name="users"),
    path('add_user_form/<int:add_button_clicked>', dashboarduserview.AddUserForm , name="add_user_form"),
    path('add_user', dashboarduserview.AddUser , name="add_user"),
    path('edit_user_form/<int:id>/<int:add_button_clicked>', dashboarduserview.EditUserForm , name='edit_user_form'), 
    path('edit_user', dashboarduserview.EditUser , name='edit_user'),
    path('user_table_custom_search', dashboarduserview.UserCustomSearch , name="user_table_custom_search"), 
    path('delete_user', dashboarduserview.DeleteUser , name="delete_user"),
    path('register_chef/<str:id>', dashboarduserview.Chefregisteration , name="register_chef"),
    path('save_admin_address/<str:add>', dashboarduserview.SaveAdminAddress , name="save_admin_address"),

    path('save_admin_auto_fill_address', Auto_fill_address_form, name='save_admin_auto_fill_address'),

    # Menus
    path('menus_categories_list', dashboardmenuview.MenuCategorieslist , name="menus_categories_list"),
    path('menu_list/<int:id>', dashboardmenuview.Menulist , name="menu_list"),
    path('add_menu_form/<int:add_button_clicked>', dashboardmenuview.AddMenuForm , name='add_menu_form'), 
    path('add_menu', dashboardmenuview.AddMenu , name='add_menu'),
    path('edit_menu_form/<int:id>/<int:add_button_clicked>', dashboardmenuview.EditMenuForm , name='edit_menu_form'),
    path('edit_menu', dashboardmenuview.EditMenu , name='edit_menu'),
    path('menu_list/delete_menu', dashboardmenuview.DeleteMenu , name="delete_menu"),
    path('menu_list/menu_list_table_custom_search', dashboardmenuview.MenuCustomSearch , name="menu_list_table_custom_search"), 
    path('menu_list/edit_menu_form/<int:id>/<int:add_button_clicked>', dashboardmenuview.EditMenuForm , name='edit_menu_form'),



    # Menu Category
    path('add_menu_category_form/<int:add_button_clicked>', dashboardmenuview.AddMenuCategoryForm , name='add_menu_category_form'), 
    path('add_menu_category', dashboardmenuview.AddMenuCategory , name='add_menu_category'),
    path('edit_menu_category_form/<int:id>/<int:add_button_clicked>', dashboardmenuview.EditMenuCategoryForm , name='edit_menu_category_form'),
    path('edit_menu_category', dashboardmenuview.EditMenuCategory , name='edit_menu_category'),
    path('delete_category', dashboardmenuview.DeleteMenuCategory , name="delete_category"),


    # Items
    path('add_item_form/<int:add_button_clicked>', dashboardmenuview.AddItemForm , name='add_item_form'), 
    path('add_item', dashboardmenuview.AddItem , name='add_item'),
    path('edit_item_form/<int:id>/<int:add_button_clicked>', dashboardmenuview.EditItemForm , name='edit_item_form'),
    path('edit_item', dashboardmenuview.EditItem , name='edit_item'),
    path('item_list', dashboardmenuview.Itemlist , name="item_list"),
    path('delete_item', dashboardmenuview.DeleteItem , name="delete_item"),
    path('edit_item_form/<int:id>/delete_item_image', dashboardmenuview.DeleteItemImage, name="delete_item_image"),
    path('item_table_custom_search', dashboardmenuview.ItemCustomSearch , name="item_table_custom_search"), 


    # Offers 
    path('add_offer_form/<int:add_button_clicked>', dashboardoffersview.AddOfferForm , name='add_offer_form'), 
    path('add_offer', dashboardoffersview.AddOffer , name='add_offer'),
    path('edit_offer_form/<int:id>/<int:add_button_clicked>', dashboardoffersview.EditOfferForm , name='edit_offer_form'),
    path('edit_offer', dashboardoffersview.EditOffer , name='edit_offer'),
    path('offers', dashboardoffersview.Offerlist , name="offers"),
    path('delete_offer', dashboardoffersview.DeleteOffer , name="delete_offer"),
    path('edit_offer_form/<int:id>/delete_offer_image', dashboardoffersview.DeleteOfferImage, name="delete_offer_image"),

    # AddOns
    path('add_addons_form/<int:add_button_clicked>', dashboardaddonsview.AddAddonsForm , name='add_addons_form'), 
    path('add_addons', dashboardaddonsview.AddAddons , name='add_addons'),
    path('edit_addons_form/<int:id>/<int:add_button_clicked>', dashboardaddonsview.EditAddonsForm , name='edit_addons_form'),
    path('edit_addons', dashboardaddonsview.EditAddons , name='edit_addons'),
    path('addons', dashboardaddonsview.Addonslist , name="addons"),
    path('delete_addons', dashboardaddonsview.DeleteAddons , name="delete_addons"),
    path('edit_addons_form/<int:id>/delete_addons_image', dashboardaddonsview.DeleteAddonsImage, name="delete_addons_image"),


    # Menu Category
    path('add_menu_category_form/<int:add_button_clicked>', dashboardmenuview.AddMenuCategoryForm , name='add_menu_category_form'), 
    path('add_menu_category', dashboardmenuview.AddMenuCategory , name='add_menu_category'),
    path('edit_menu_category_form/<int:id>/<int:add_button_clicked>', dashboardmenuview.EditMenuCategoryForm , name='edit_menu_category_form'),
    path('edit_menu_category', dashboardmenuview.EditMenuCategory , name='edit_menu_category'),
    path('delete_category', dashboardmenuview.DeleteMenuCategory , name="delete_category"),
    path('edit_item_form/<int:id>/delete_item_image', dashboardmenuview.DeleteItemImage, name="delete_item_image"),


    # Menu Item Detail
    path('menu_item_detail/<int:id>', dashboardmenuview.MenuItemDetail , name='menu_item_detail'),
    path('add_associated_item_form/<int:id>/<int:counter>', dashboardmenuview.AddAssociatedItemMenuForm , name='add_associated_item_form'),
    path('add_associated_item', dashboardmenuview.AddAssociatedItemMenu , name='add_associated_item'),
    path('edit_associated_item_form/<int:id>/<int:counter>', dashboardmenuview.EditAssociatedItemMenuForm , name='edit_associated_item_form'),
    path('edit_associated_item', dashboardmenuview.EditssociatedItemMenu , name='edit_associated_item'),  


    # Order Listing
    path('order_item_listing_page', dashboardmenuview.OrderItemsListingPage , name='order_item_listing_page'),
    path('item_order_placing_form/<int:id>/<int:add_button_clicked>', dashboardmenuview.ItemOrderForm , name='item_order_placing_form'),
    path('place_order', dashboardmenuview.SubmitItemOrderForm , name='place_order'),
    path('confirm_order_payment', dashboardordersview.confirmorderpayment, name='confirm_order_payment'),
    path('order_confirmation/<int:id>', dashboardmenuview.OrderConfirmation, name='order_confirmation'),



    # System Modules
    path('systemmodules', dashboardsystemmodulesview.SystemModulesList , name='systemmodules'), 
    path('add_systemmodule_form/<int:add_button_clicked>', dashboardsystemmodulesview.AddSystemModuleForm , name='add_systemmodule_form'),
    path('add_systemmodule', dashboardsystemmodulesview.AddSystemModule , name='add_systemmodule'),
    path('edit_systemmodule_form/<int:id>/<int:add_button_clicked>', dashboardsystemmodulesview.EditSystemModuleForm , name='edit_systemmodule_form'),
    path('edit_systemmodule', dashboardsystemmodulesview.EditSystemModule , name='edit_systemmodule'),
    path('delete_module', dashboardsystemmodulesview.DeleteSystemModule , name="delete_module"),

    # FoodApp Setting
    path('foodapp_setting', dashboardsystemmodulesview.FoodappSetting , name="foodapp_setting"),
    path('edit_foodapp_setting', dashboardsystemmodulesview.EditFoodappSetting , name="edit_foodapp_setting"),
    
    # Web Dynamic Content
    path('web_dynamic_content_form', dashboardsystemmodulesview.WebDynamicContentForm , name="web_dynamic_content_form"),
    path('edit_web_dynamic_content', dashboardsystemmodulesview.EditWebDynamicContent , name="edit_web_dynamic_content"),

    # Our Service Web Content
    path('service_title_form', dashboardsystemmodulesview.ServicesSectionForm , name="service_title_form"),
    path('edit_service_section_form', dashboardsystemmodulesview.EditServicesSectionForm , name="edit_service_section_form"),
    # Service 
    path('add_service_form/<int:add_button_clicked>', dashboardserviceview.AddServiceForm , name='add_service_form'), 
    path('add_service', dashboardserviceview.AddService , name='add_service'),
    path('edit_service_form/<int:id>/<int:add_button_clicked>', dashboardserviceview.EditServiceForm , name='edit_service_form'),
    path('edit_service', dashboardserviceview.EditService , name='edit_service'),
    path('service_list', dashboardserviceview.Servicelist , name="service_list"),
    path('delete_service', dashboardserviceview.DeleteService , name="delete_service"),

    # Client Section
    path('client_section_form', dashboardclientsview.ClientSectionForm , name="client_section_form"),
    path('edit_client_section_form', dashboardclientsview.EditClientSectionForm , name="edit_client_section_form"),
    # OurClients 
    path('add_testimonial_form/<int:add_button_clicked>', dashboardclientsview.AddTestimonialForm , name='add_testimonial_form'), 
    path('add_testimonial', dashboardclientsview.AddTestimonial , name='add_testimonial'),
    path('edit_testimonial_form/<int:id>/<int:add_button_clicked>', dashboardclientsview.EditTestimonialForm , name='edit_testimonial_form'),
    path('edit_testimonial', dashboardclientsview.EditTestinomial , name='edit_testimonial'),
    path('testimonial_list', dashboardclientsview.Testimoniallist , name="testimonial_list"),
    path('delete_testimonial', dashboardclientsview.DeleteTestimonial , name="delete_testimonial"),

    # Rider Commision Settings
    path('rider_commision_form', dashboardriderview.RiderCommisionForm , name="rider_commision_form"),
    path('edit_rider_commision_form', dashboardriderview.EditRiderCommisionForm , name="edit_rider_commision_form"),

    # Order
    path('orders', dashboardordersview.Orderlist , name='orders'), 
    path('order_detail/<int:id>', dashboardordersview.OrderDetail , name='order_detail'), 
    path('order_table_custom_search', dashboardordersview.OrderCustomSearch , name="order_table_custom_search"), 
    path('my_kitchen_order_table_custom_search', dashboardordersview.MyKitchenOrderCustomSearch , name="my_kitchen_order_table_custom_search"), 
    path('previous_orders', dashboardordersview.PreviousOrderlist , name='previous_orders'), 
    path('add_order_notes_form/<int:id>/<int:add_button_clicked>', dashboardordersview.AddOrderNotesForm , name='add_order_notes_form'),
    path('add_order_notes', dashboardordersview.AddOrderNote , name='add_order_notes'),
    path('rider_pending_orders', dashboardordersview.PendingRiderOrderlist , name='rider_pending_orders'),
    path('assign_rider_orders', dashboardordersview.AssignRiderPendingOrders , name='assign_rider_orders'),
    path('add_order_notes_modal', dashboardordersview.AddOrderNoteModal, name="add_order_notes_modal"),
    path('fetch_order_notes_modal', dashboardordersview.FetchOrderNoteModal, name="fetch_order_notes_modal"),




    # Payment Accounts
    path('add_payment_account_form/<int:add_button_clicked>', dashboardpaymentaccountview.AddPaymentAccountForm , name='add_payment_account_form'),
    path('add_payment_account', dashboardpaymentaccountview.AddPaymentAccount , name='add_payment_account'),
    path('edit_payment_account_form/<int:id>/<int:add_button_clicked>', dashboardpaymentaccountview.EditPaymentAccountForm , name='edit_payment_account_form'),
    path('edit_payment_account', dashboardpaymentaccountview.EditPaymentAccount , name='edit_payment_account'),
    path('payment_accounts', dashboardpaymentaccountview.PaymentAccountList , name='payment_accounts'),
    path('delete_payment_account', dashboardpaymentaccountview.DeletePaymentAccount , name="delete_payment_account"),
    path('all_payment_account_list', dashboardpaymentaccountview.AllPaymentAccountslist , name="all_payment_account_list"),
    path('payment_account_table_custom_search', dashboardpaymentaccountview.PaymentAccountCustomSearch , name="payment_account_table_custom_search"), 
    path('my_payment_account_table_custom_search', dashboardpaymentaccountview.MyPaymentAccountCustomSearch , name="my_payment_account_table_custom_search"), 
    path('kitchen_payment_share', dashboardpaymentaccountview.KitchenPaymentShare , name="kitchen_payment_share"), 
    path('upd_kitchen_payment_share_status', dashboardpaymentaccountview.UpdateKitchenPaymentShareStatus , name='upd_kitchen_payment_share_status'),
    path('kitchen_accounts_detail_list/<int:id>', dashboardpaymentaccountview.KitchenAccountsDetaillist, name="kitchen_accounts_detail_list"),

    # Order Status
    path('add_order_status_form/<int:add_button_clicked>', dashboardorderstatusview.AddOrderStatusForm , name='add_order_status_form'),
    path('add_order_status', dashboardorderstatusview.AddOrderStatus , name='add_order_status'),
    path('edit_order_status_form/<int:id>/<int:add_button_clicked>', dashboardorderstatusview.EditOrderStatusForm , name='edit_order_status_form'),
    path('edit_order_status', dashboardorderstatusview.EditOrderStatus , name='edit_order_status'),
    path('order_status', dashboardorderstatusview.OrderStatusList , name='order_status'), 
    path('edit_order_status_notif', dashboardorderstatusview.EditOrderStatusNotif , name='edit_order_status_notif'),
    path('delete_order_status', dashboardorderstatusview.DeleteOrderStatus , name='delete_order_status'), 
    path('edit_order_status_notif_search', dashboardorderstatusview.EditOrderStatusNotifSearch , name='edit_order_status_notif_search'),


    #JWT Auth Endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    #Tok Status Api's
    path('api/get_tok_status', Users_apis_view.GetTokStatus.as_view(), name="get_tok_status"),


    #kitchens  Api's      *******

    #Verify  kitchen Api
    path('api/verify_kitchen', Users_apis_view.VerifyKitchen.as_view(), name="verify_kitchen_api"), 

    path('api/save_kitchen_details', SaveKitchen.as_view(), name="save_kitchen_details_api"),
    path('api/update_kitchen_details', UpdateKitchen.as_view(), name="update_kitchen_details_api"),
    path('api/save_kitchen_speciality', SaveKitchenSpeciality.as_view(), name="save_kitchen_speciality_api"),
    path('api/save_kitchen_availblity', SaveKitchenavailblity.as_view(), name="save_kitchen_availblity_api"),
    path('api/get_my_kitchen_details/<int:user_id>', GetMyKitchenDetails.as_view(), name="get_my_kitchen_details_api"),
    path('api/get_my_kitchen_orders/<int:user_id>', GetMyKitchenOrders.as_view(), name="get_my_kitchen_orders_api"),
    path('api/get_my_kitchen_menu_orders/<int:user_id>', GetMyKitchenMenuOrders.as_view(), name="get_my_kitchen_menu_orders_api"),
    path('api/change_order_status', SaveOrderStatus.as_view(), name="change_order_status_api"),

    path('api/get_kitchen_order_statuses', GetKitchenOrderstatuses.as_view(), name="get_kitchen_order_statuses_api"),

    path('api/kitchen_paymentaccount/<int:user_id>', KitchenPaymentsApi.as_view(), name="kitchen_paymentaccount_api"),
   
    #my kitchen all orders
    path('api/get_my_kitchen_all_orders/<int:user_id>', GetMyKitchenCurrentallOrders.as_view(), name="get_my_kitchen_all_orders_api"),

    #kitchen cooked orders
    path('api/get_my_kitchen_cooked_orders/<int:user_id>', GetMyKitchenCookedOrders.as_view(), name="get_my_kitchen_cooked_orders_api"),


    #User Api's      *******

    #User logout Api
    path('api/logout', Users_apis_view.LogoutfromApp.as_view(), name="logout_app"),

    #customer Registration 
    path('api/register_customer', Users_apis_view.RegisterCustomer.as_view(), name="register_customer_api"), 

    #customer Login 
    path('api/login_customer', Users_apis_view.LoginCustomer.as_view(), name="login_customer_api"),


    #Food  Api's   *******


    #Get Daily Food  Api
    path('api/get_daily_food', GetDailyFoodItems.as_view(), name="get_daily_food_api"),

    #Get Adds on  Api
    path('api/get_adds_on', GetAddsonItems.as_view(), name="get_adds_on_api"),

    #Get All Menus  Api
    path('api/get_all_menus', GetAllMenus.as_view(), name="get_all_menus_api"),

    #Get Single Item Api
    path('api/get_single_food_item/<int:id>', GetSingleFoodItems.as_view(), name="get_single_food_item_api"),


    #Get Single Menu Api
    path('api/get_menu/<int:id>', GetMenuFood.as_view(), name="get_menu_api"),


    #Orders  Api's      *******

    #Place order api
    path('api/place_order', SaveFoodOrder.as_view(), name="place_order_api"),

    #Place menu order api
    path('api/place_menu_order', SaveMenuOrder.as_view(), name="place_menu_order_api"),
    
    #get  my orders api
    path('api/get_my_orders/<str:my_email>', GetmyOrders.as_view(), name="get_my_orders_api"),

    #get  my all  orders api
    path('api/get_my_all_orders/<str:my_email>', GetmyallOrders.as_view(), name="get_my_all_orders_api"),

    #get my  menu order api
    path('api/get_my_menu_order/<str:my_email>', GetmyMenuOrders.as_view(), name="get_my_menu_order_api"),

    #get single order api
    path('api/get_single_order/<int:order_id>', GetSingleOrder.as_view(), name="get_single_order_api"),

    #Payments Api's      *******

    #admin payment accounts
    path('api/get_admin_accounts', Users_apis_view.GetPaymentSettings.as_view(), name="get_admin_accounts_api"),

    
    #Kitchen orders payments
    path('api/Kitchen_orders_payments/<int:kitchen_id>', GetKitchenOrdersPaymentsUpdated.as_view(), name="Kitchen_orders_payments_api"),


    #Rider   api's  *******

    #register rider
    path('api/register_rider', Users_apis_view.RegisterRider.as_view(), name="register_rider_api"),

    #get  rider  details
    path('api/get_rider_details/<str:email>', Users_apis_view.GetRiderDeatils.as_view(), name="get_rider_details_api"),

    #rider availability
    path('api/save_rider_availblity', Users_apis_view.SaveRideravailblity.as_view(), name="save_rider_availblity_api"),

    #rider  order  pickup
    path('api/rider_order_pickup/<str:email>', Users_apis_view.GetRiderOrders.as_view(), name="rider_order_pickup_api"),

    #rider  order  delivered
    path('api/rider_order_delivered/<str:email>', Users_apis_view.GetRiderDeliveredOrders.as_view(), name="rider_order_delivered_api"),
   
    #Rider update ordder Status
    path('api/rider_change_order_status', RiderUpdateOrderStatus.as_view(), name="rider_change_order_status_api"),


    #Rider orders payments
    path('api/rider_orders_payments/<str:email>', GetRiderDeliveryPayments.as_view(), name="rider_orders_payments_api"),

   
    #Others     ************

    #Get Website Dynamics
    path('api/get_website_dynamics', Users_apis_view.GetWebsiteDynamics.as_view(), name="get_website_dynamics_api"),

    #Get our services
    path('api/get_our_services', Users_apis_view.GetOurServices.as_view(), name="get_our_services_api"),

    #Get our clients
    path('api/get_our_clients', Users_apis_view.GetOurClients.as_view(), name="get_our_clients_api"),



    # Cart Api's   ***********

    # Save Cart
    path('api/save_cart', CartOrder.as_view(), name="save_cart_api"),




    # Search Api's  **********************************

 
    #Search Api
    path('api/search/<str:key>', GetSearch.as_view(), name="search"), 


    #  Newsletter Api 

    path('api/newsletter', Newsletter.as_view(), name="newsletter"),


    # Deals  Api's   ***********

    #GetDeals Api 
    path('api/get_deals', GetDeals.as_view(), name="get_deals_api"),

]