
from exponent_server_sdk import (
    DeviceNotRegisteredError,
    PushClient,
    PushMessage,
    PushServerError,
    PushTicketError,
)
import os
import requests
from requests.exceptions import ConnectionError, HTTPError 

# from webApp.models import PushToken


session = requests.Session()
session.headers.update(
    {
        "Authorization": "Bearer MK0Fix5NY8WqDmvxkahZ7nvVsQ8gACuNfkvJg5s_",
        "accept": "application/json",
        "accept-encoding": "gzip, deflate",
        "content-type": "application/json",
    }
)

def send_push_message(token, message, extra, channel_id="default", display_in_foreground= True):
    try:
        response = PushClient(session=session).publish(
            PushMessage(to=token, body=message, data=extra,channel_id=channel_id,display_in_foreground=display_in_foreground)
            
        )

        print( "1st success")
    except PushServerError as exc:
        # Handle push server error (log it, report it, etc.)
        print("error 000", exc)
        print("Push server error:", exc.errors)
        print("Response data:", exc.response_data)
        raise
    except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError) as exc:
        # Handle connection or HTTP error

        print("error 111 connection")
        raise

    try:
        response.validate_response()
    except DeviceNotRegisteredError:
        print("Devie not registered ")
        # PushToken.objects.filter(token=token).update(active=False)
    except PushTicketError as exc:
        print("error except 22")
        print(exc)
        raise


# def send_salient_data_message(token, extra,channel_id="silent",priority="high",sound=None,badge=None):
#     try:
#         response = PushClient(session=session).publish(
#             PushMessage(to=token,title=None, channel_id=channel_id,body=None,data=extra,priority=priority,sound=sound,badge=badge)
            
#         )

#         print( "1st success")
#     except PushServerError as exc:
#         # Handle push server error (log it, report it, etc.)
#         print("error 000", exc)
#         print("Push server error:", exc.errors)
#         print("Response data:", exc.response_data)
#         raise
#     except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError) as exc:
#         # Handle connection or HTTP error

#         print("error 111 connection")
#         raise

#     try:
#         response.validate_response()
#     except DeviceNotRegisteredError:
#         print("Devie not registered ")
#         # PushToken.objects.filter(token=token).update(active=False)
#     except PushTicketError as exc:
#         print("error except 22")
#         print(exc)
#         raise


def send_salient_data_message(token, extra,priority= "high"):
    try:
        # Send the push notification with `content_available` set to True
        response = PushClient().publish(
            PushMessage(
                to=token,
                data=extra,
                priority = priority
                          
            )
        )
        print("Data notification sent successfully.")

    except PushServerError as exc:
        print("Push server error:", exc.errors)
        print("Response data:", exc.response_data)
        raise
    except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError) as exc:
        print("Connection error:", exc)
        raise

    try:
        response.validate_response()
    except DeviceNotRegisteredError:
        print("Device not registered.")
        # Optional: deactivate token in your database
    except PushTicketError as exc:
        print("Push ticket error:", exc)
        raise





import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def send_notification_view(request):
    # Check if the request method is POST
    if request.method == 'POST':
        try:
            # Load JSON data from the request body
            data = json.loads(request.body)

            # Extract the values
            token = data.get('token')
            message = data.get('message')
            extra = data.get('extra', None)

            # Debug prints
            print(f"Token: {token}")
            print(f"Message: {message}")
            print(f"Extra: {extra}")

            # Call the function to send the push notification
            print("Sending push notification...")
            send_push_message(token, message, extra)
            print("Notification sent successfully.")

            return JsonResponse({'status': 'success'})

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed.'}, status=405)




@csrf_exempt
def send_data_notification_view(request):
    # Check if the request method is POST
    if request.method == 'POST':
        try:
            # Load JSON data from the request body
            data = json.loads(request.body)

            # Extract the values
            token = data.get('token')
            # message = data.get('message')
            extra = data.get('extra')
            
            # extra = data.get('extra', None)

            # Debug prints
            print(f"Token: {token}")

            # print(f"Message: {message}")
            
            print(f"Extra: {extra}")

            # Call the function to send the push notification
            print("Sending data notification...")
            send_salient_data_message(token, extra)
            print("data Notification sent successfully.")

            return JsonResponse({'status': 'success'})

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed.'}, status=405)
