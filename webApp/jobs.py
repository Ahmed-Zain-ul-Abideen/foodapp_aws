from schedule import Scheduler
import threading
import time 
from .models import *
from  webApp.views.Others.geocode_address import lat_long_nearest_rider 
from django.shortcuts import get_object_or_404
from webApp.views.expo_notif_view import send_push_message,send_salient_data_message
from  webApp.views.Others.geocode_address   import  distance_in_km
from webApp.utils  import truncate_float

from django.utils import timezone
def give_admin_gold():
    print("Schedule streak")
    try: 
        print("scheduling success")
        print("    ")
        print("    ")
        print("    ")
        print("  --------  ")
        print("    ",timezone.now())
        print("    ")
        if  Orders.objects.filter(rider_pending=True).exists():
            try:
                orders = Orders.objects.filter(rider_pending=True)
                for  order in orders:
                    order.rider_pending = False
                    order.save()
                list_no_order = []
                for  order in orders:
                    kitchen_info = KitchenAddress.objects.filter(Kitchen_id__in= list(Orders.objects.filter(pk=order.pk).values_list('kitchen_id',flat=True))).first()
                 
                    rider, the_distance = lat_long_nearest_rider(kitchen_info.latitude,kitchen_info.longitude)
                    print("rider for notif scedule",rider,' the_distance',the_distance)
                    if  rider  is  None:
                        list_no_order.append(order.pk)
                    else:
                        order_rads = Orders.objects.filter(pk=order.pk).first()
                        the_distance  =  float(the_distance)  +   float(order_rads.kitchen_to_customer_distance)
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
                            order_id= order.pk,
                            rider_share_amount = truncate_float(calc_dist,2)
                        )
                        RiderOrders.objects.create(rider_id=rider,order_id=order.pk,delivery_distance=the_distance)
                        # Orders.objects.filter(pk=order.pk).update(status="ready_for_pickup")
                        order_rads.status = "ready_for_pickup"
                        order_rads.save()
                        rider_pk = get_object_or_404(RiderDetails.objects.only('registration_id'), pk=rider) 
                        send_push_message(rider_pk.registration_id, "Ready for Pickup: Your Next Delivery Awaits!", {"link": "/(tabs)/order"})
                        try: 
                            extra = {"newData": "1"}
                            send_salient_data_message(rider_pk.registration_id, extra)
                        except Exception as e:
                            print("Error sending silent message to Rider:", e)
                        
                        try:
                            customer_fcm = get_object_or_404(Orders.objects.only('order_fcm'), pk=order.pk) 
                            send_push_message(customer_fcm.order_fcm, "Hot and Fresh! Your Order is Ready for Pickup/Delivery.", {"link": "/(tabs)/pastOrders/" + str(order.pk)} ) 
                        except:
                            print("order ready for pickup to customer  notif in cronjob send fail")
                if len(list_no_order):
                    print("ins chedule again no rider list for orders",list_no_order)
                    Orders.objects.filter(pk__in=list_no_order).update(rider_pending=True)


            except Exception as e:
                print("excpetion in pending orders",e)
        else:
            print("No rider pending orders")

        print("    ") 
    except Exception as e:
        print("error in scheduling because",e)





def run_continuously(self, interval=1):
    """Continuously run, while executing pending jobs at each elapsed
    time interval.
    @return cease_continuous_run: threading.Event which can be set to
    cease continuous run.
    Please note that it is *intended behavior that run_continuously()
    does not run missed jobs*. For example, if you've registered a job
    that should run every minute and you set a continuous run interval
    of one hour then your job won't be run 60 times at each interval but
    only once.
    """

    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):

        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                self.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.setDaemon(True)
    continuous_thread.start()
    return cease_continuous_run

Scheduler.run_continuously = run_continuously

def start_scheduler():
    scheduler = Scheduler()
    scheduler.every().minute.do(give_admin_gold)
    scheduler.run_continuously()