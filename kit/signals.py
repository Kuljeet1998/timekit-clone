from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.db.models.signals import post_save, pre_save
from .models import *
from django.dispatch import receiver
import sendgrid
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import http.client
from urllib.parse import urlencode
import requests
import json

# @receiver(post_save,sender=OneToOneBooking)
# def send_mail_to_user(sender, instance, created,**kwargs):
#     if created:
#         conn = http.client.HTTPSConnection("api.sendgrid.com")

#         data = {
#                     "personalizations": [
#                     {
#                       "to": [
#                         {
#                           "email":"kuljeetsingh_1998@rediffmail.com"
#                         }
#                       ],
#                       "dynamic_template_data":{
#                             "name":instance.project.slot_setting.name,
#                             "location":instance.project.slot_setting.location,
#                             "username":instance.booked_by.user.email,
#                             "start":str(instance.start_date_time),
#                             "end":str(instance.end_date_time)
#                       },
#                       "subject": "Booking"
#                     }
#                   ],
#                     "from": {
#                     "email": "kbhengura@gmail.com"
#                   },
#                   "template_id": "d-dbcb131007544e4897ab67398e30ddef",
#                 }



#         headers = {
#                     'authorization': "Bearer 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",
#                     'content-type': "application/json"
#                 }

#         url = "https://api.sendgrid.com/v3/mail/send"
#         response = requests.request("POST", url, data=json.dumps(data), headers=headers)
#         print(response.text)

@receiver(post_save,sender=OneToOneBooking)
def trigger_webhook(sender, instance, created,**kwargs):
    if created:
        webhook, created = WebhookTarget.objects.get_or_create(customer=instance.booked_by,event="test")
        url = webhook.url+"asd"
        response = requests.request("GET", url)
        if response.status_code == 200:
            log = Log.objects.create(webhook_target=webhook,
                                    response_status=response.status_code,
                                    attempt=1,
                                    is_sent=True)
        else:
            log = Log.objects.create(webhook_target=webhook,
                                        attempt=1,
                                        response_status=response.status_code)
            for attempt in range(1,3):
                response = requests.request("GET", url+"asd")
                log.attempt +=1
                log.save()
                if response.status_code==200:
                    log.is_sent=True
                    log.save()
                    break

# @receiver(post_save,sender=Log)
# def create_logs(sender, instance, created,**kwargs):
#     if created:
#         is_sent = instance.is_sent
#         if is_sent==False:
#             url = instance.webhook_target.url
#             for attempt in range(1,3):
#                 import pdb;
#                 pdb.set_trace()
#                 response = requests.request("GET", url)
#                 instance.attempt +=1
#                 if response.status_code==200:
#                     instance.is_sent=True
#                     break