from fcm_django.models import FCMDevice
from webApp.models import * 
 
from firebase_admin import messaging  

def send_kitchen_notification_fcmi(notif_data):
    try:  
        #registration_tokens  = list(FCMDevice.objects.filter(active=1).filter(user_id__in=notif_data['users']).values_list('registration_id',flat=True))
        registration_tokens  =  notif_data['registration_tokens']
        if len(registration_tokens): 
            message = messaging.MulticastMessage(
                notification=messaging.Notification(
                    title=notif_data['title'],
                    body=notif_data['text'], 
                    image = notif_data['session_image'],  
                
                ),
                apns = messaging.APNSConfig(
                    payload=messaging.APNSPayload(
                        aps=messaging.Aps(  
                            sound= "default"
                        ),
                    ),
                ),
                data={
                    'id': str(notif_data['id']),
                    'type': 'notification', 
                },
                tokens=registration_tokens
            )

            response = messaging.send_each_for_multicast(message) 
    except Exception as e:
        print("new cont notif error",e)
    return True

def send_order_notification_fcmi(notif_data):
    try:  
        # registration_tokens  = list(Orders.objects.filter(pk__in=notif_data['orders']).values_list('order_fcm',flat=True))
        registration_tokens  =  notif_data['registration_tokens']
        if len(registration_tokens): 
            message = messaging.MulticastMessage(
                notification=messaging.Notification(
                    title=notif_data['title'],
                    body=notif_data['text'], 
                    image = notif_data['session_image'],  
                
                ),
                apns = messaging.APNSConfig(
                    payload=messaging.APNSPayload(
                        aps=messaging.Aps(  
                            sound= "default"
                        ),
                    ),
                ),
                data={
                    'id': str(notif_data['id']),
                    'type': 'notification', 
                },
                tokens=registration_tokens
            )

            response = messaging.send_each_for_multicast(message) 
    except Exception as e:
        print("web order notif error",e)
    return True