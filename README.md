# How to handle AWS bounces and complaints with Python (Django)

### Why handle bounces and complaints?

You probably own a domain name with which you want to send emails with by using Amazon's SES. Bounce and complaints are responses given if an email couldn't be delivered, surely you had a similar situation where in your personal email address you tried to send someone an email and you got an automatic response telling you the email couldn't be delivered (usually because of a typo in the email address). Why it's practical: if you own an email list of your subscribers, you can keep it up to date thanks to these notifications, a bounce/reject could allow you to remove that email from your list and avoid sending an email to that address again.

Furthermore __it's an SES requirement to handle these bounces and complaints.__

## Pre-requisites:
- Have an AWS account
- Have a verified domain name on SES under domains in identity manager
- Something your Amazon can send its requests to, I use a django website

## Step 1: Create a topic
 
Go to Amazon Simple Notification Service (SNS) and create a topic, call it whatever you want, I used the name of my domain underscore topic (domain_topic). You can leave out all other options as default.

![Create topic](/assets/1.png)

## Step 2: Subscribe to the topic
### a: Set up a view
Now we need to have a way for our AWS notification to arrive to us and to subscribe to the topic. In my case I used Django as I find it easier to set up, but if you find a way to receive these requests in python, then go ahead and skip the first part. I will explain how to do it with Django.

I assume you know how to set up a [django website](https://docs.djangoproject.com/en/3.0/intro/tutorial01/) and that you probably have [hosted it](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html). In this case I created a new view under `views.py` and called it bounce_handler as such:
```
from django.http import JsonResponse
import urllib.request
import json

@csrf_exempt
def bounce_handler(request):
    if request.body.decode("utf-8"):
         urllib.request.urlopen(json.loads(request.body)['SubscribeURL']) # Confirms subscription
         
    return JsonResponse({})
```
Make sure to save that, don't forget to add it to your `urls.py` file, I personally gave my bounce_handler view the /bounce_handler url. Finally, deploy your website.


### b: Send a subscription url
Once this is done, we then need to confirm the subscription. Amazon will send you a subscription link as a request to your new url, when clicking on it, amazon will confirm the subscription. To do that you need to go to your new SNS topic and click on "create subscription", select the protocol, in my case I will use HTTPS as I have set up HTTPS for my website, use HTTP if your website doesn't have HTTPS, and in endpoint, you need to put in the bounce_handler full url.

![Create Subscription](/assets/2.jpg)

Once you've done this, it should confirm automatically. Otherwise, make sure the code is like above, redeploy, and click on request confirmation in your topic, this should send a request to your bounce_handler view, which will then confirm the subscription. Wait a bit and you should see that the subscription has been confirmed under status.

![Confirm Subscription](/assets/3.jpg)

## Step 3: Handling Bounces and Complaints
Great! We are almost done, go back to your `views.py` file and change the code that we wrote earlier and put in your own code. Below is an example, it doesn't do anything except assigning variables, it's just to show you that you can use these variables for whatever you want and to show you what the json format would look like.

```
from django.http import JsonResponse
import json

@csrf_exempt
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
```

You can now handle bounces and complaints, all we need to do now is go back to our SES dashboard. Go to domains, click the domain you want to send emails with, under notifications click 'edit configuration', and under 'bounces' and 'complaints' select your topic you created ealier.

![Select topic in configuration](/assets/4.png)

And that's it! Any bounces or complaints will be sent to your bounce url.

If you want to test it, use `bounce@simulator.amazonses.com`, this email will automatically bounce any email you send it to.

![Send test email](/assets/5.jpg)
