from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
from webApp.models  import *

# @receiver(post_save, sender=Orders)
# def model_change_notification(sender, instance, **kwargs):
#     print("chanel signal fired")
#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(
#         'notifications_group',
#         {
#             'type': 'send_order_notification',
#             'message': f'Model {sender.__name__} has been updated!'
#         }
#     )