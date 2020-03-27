from django.http import JsonResponse
import urllib.request
import json

'''
# Step 2.a.
def bounce_handler(request):
    if request.body.decode("utf-8"):
        urllib.request.urlopen(json.loads(request.body)['SubscribeURL']) # Confirms subscription
        
    return JsonResponse({})
'''

# Step 3
from django.http import JsonResponse
import json

def bounce_handler(request):
    if request.body.decode("utf-8"):
        # Do something with the data
        message = json.loads(json.loads(request.body)['Message'])
        notification_type = message['notificationType']
        recipients = message['bounce']['bouncedRecipients']
        for recipient in recipients:
            email_address = recipient['emailAddress']
            action = recipient['action'] # e.g. 'failed'
        from_email = message['mail']['source']
        timestamp = message['mail']['timestamp']
        
    return JsonResponse({})
