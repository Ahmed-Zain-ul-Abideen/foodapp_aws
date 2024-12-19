from django.urls import re_path
from   webApp.consumers import   *

websocket_urlpatterns = [
    re_path(r'ws/notifications/$', OrderConsumer.as_asgi()),
    re_path(r'ws/notifications_listing_pag/$', OrderListingConsumer.as_asgi()),
]