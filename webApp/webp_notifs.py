from pywebpush import webpush, WebPushException
from django.conf import settings

def send_to_website_push_notification(subscription_info, message):
    try:
        webpush(
            subscription_info=subscription_info,
            data=message,
            vapid_private_key=settings.VAPID_PRIVATE_KEY,
            vapid_public_key=settings.VAPID_PUBLIC_KEY,
            vapid_claims={
                "sub": f"mailto:{settings.VAPID_EMAIL}"
            }
        )
    except WebPushException as ex:
        print(f"Failed to send notification to website : {ex}")