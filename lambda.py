import os
import json
import requests
from datetime import datetime, timedelta, time
import pytz

INTERCOM_ACCESS_TOKEN = os.environ["INTERCOM_ACCESS_TOKEN"]
ADMIN_URL = os.environ["ADMIN_URL"]

WORK_HOURS_START = time(8, 0)
WORK_HOURS_END = time(17, 0)
TIMEZONE = pytz.timezone('Africa/Lagos')  # Adjust the timezone as needed

def is_work_hours():
    now = datetime.now(TIMEZONE).time()
    day_of_week = datetime.now(TIMEZONE).weekday()  # Monday is 0 and Sunday is 6
    return WORK_HOURS_START <= now <= WORK_HOURS_END and day_of_week < 5

def admin_id():
    headers = {
        "Intercom-Version": "2.11",
        "Authorization": f"Bearer {INTERCOM_ACCESS_TOKEN}"
    }
    response = requests.get(ADMIN_URL, headers=headers)
    data = response.json()["id"]
    return data

def send_message_during_office_hours(conversation_id, admin_id, user_name=None):
    message_data = {
        "message_type": "comment",
        "type": "admin",
        "admin_id": f"{admin_id}",
        "body": (
            f"<p class=\"no-margin\">Hello {user_name} 👋,</p>\n\n"
            "<p class=\"no-margin\">Thank you for reaching out to Kredete.</p>\n\n"
            "<p class=\"no-margin\">We want you to know that we have received your message and truly appreciate your patience. Please feel free to provide any additional details or images that might help us assist you better. Thank you for your understanding and patience.</p>\n\n"
            "<p class=\"no-margin\">Best regards,</p>\n\n"
            "<p class=\"no-margin\"><b>Kredete CX Team</b></p>"
        )
    }
    headers = {
        'Authorization': f'Bearer {INTERCOM_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    response = requests.post(f'https://api.intercom.io/conversations/{conversation_id}/reply', headers=headers, json=message_data)
    if response.status_code == 200:
        print("In-office message sent successfully.")
    else:
        print("Failed to send in-office message. Status code:", response.status_code)

def send_out_of_office_message(conversation_id, admin_id, user_name=None):
    message_data = {
        "message_type": "comment",
        "type": "admin",
        "admin_id": f"{admin_id}",
        "body": (
            f"<p class=\"no-margin\">Hello {user_name} 👋,</p>\n\n"
            "<p class=\"no-margin\">Thank you for contacting us. We are currently offline, but your message is important to us.</p>\n\n"
            "<p class=\"no-margin\">Our office hours are:<b> </b></p>\n\n"
            "<p class=\"no-margin\">Monday to Friday: <b>8AM - 5PM</b> <b>WAT</b></p>\n\n"
            "<p class=\"no-margin\">Saturday: <b>9AM - 2PM WAT </b></p>\n\n"
            "<p class=\"no-margin\">During this time, we are committed to providing you with exceptional support.</p>\n\n"
            "<p class=\"no-margin\">Kindly leave a message about your issue, and one of our dedicated team members will get back to you momentarily.</p>\n\n"
            "<p class=\"no-margin\">Alternatively, you may find the answers to your questions in our comprehensive <b>FAQ</b> section on our website.</p>\n\n"
            "<p class=\"no-margin\"><a href=\"https://www.kredete.com/faq\">https://www.kredete.com/faq</a></p>\n\n"
            "<p class=\"no-margin\">Best regards,</p>\n\n"
            "<p class=\"no-margin\"><b>Kredete CX Team</b></p>"
        )
    }
    headers = {
        'Authorization': f'Bearer {INTERCOM_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    response = requests.post(f'https://api.intercom.io/conversations/{conversation_id}/reply', headers=headers, json=message_data)
    if response.status_code == 200:
        print("Out-of-office message sent successfully.")
    else:
        print("Failed to send out-of-office message. Status code:", response.status_code)
        
def send_alert_message(conversation_id, admin_id, user_name=None):
    message_data = {
        "message_type": "comment",
        "type": "admin",
        "admin_id": f"{admin_id}",
        "body": (
            f"<p class=\"no-margin\">Hi {user_name},</p>\n\n"
            "<p class=\"no-margin\">currently there is a delay with issuing of account numbers. We are currently working on the issue to provide a resolve as quickly as possible.</p>\n\n"
            "<p class=\"no-margin\">While this may not be ideal, we implore you to please exercise some patience while we look into the issue.</p>\n\n"
            "<p class=\"no-margin\">Regards,</p>\n\n"
            "<p class=\"no-margin\"><b>Kredete CX Team</b></p>"
        )
    }
    headers = {
        'Authorization': f'Bearer {INTERCOM_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    response = requests.post(f'https://api.intercom.io/conversations/{conversation_id}/reply', headers=headers, json=message_data)
    if response.status_code == 200:
        print("Out-of-office message sent successfully.")
    else:
        print("Failed to send out-of-office message. Status code:", response.status_code)        

def snooze_conversation(conversation_id, admin_id):
    now = datetime.now(TIMEZONE)
    day_of_week = now.weekday()

    if day_of_week < 4:  # Monday to Thursday
        snooze_until = now + timedelta(days=1)
    elif day_of_week == 4:  # Friday
        snooze_until = now + timedelta(days=3)
    else:  # Saturday and Sunday
        snooze_until = now + timedelta(days=(7 - day_of_week))

    snooze_until = snooze_until.replace(hour=9, minute=0, second=0, microsecond=0)
    epoch_time = int(snooze_until.timestamp())

    snooze_data = {
        "message_type": "snoozed",
        "admin_id": f"{admin_id}",
        "snoozed_until": epoch_time
    }

    headers = {
        'Authorization': f'Bearer {INTERCOM_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    response = requests.post(f'https://api.intercom.io/conversations/{conversation_id}/parts', headers=headers, json=snooze_data)
    if response.status_code == 200:
        print("Conversation snoozed successfully.")
    else:
        print("Failed to snooze conversation. Status code:", response.status_code)

admin_id = admin_id()

# if is_work_hours():
#     send_message_during_office_hours(conversation_id="5047", admin_id=admin_id)
# else:
#     send_out_of_office_message(conversation_id="5042", admin_id=admin_id, user_name="Ajani Oshodi")
#     snooze_conversation(conversation_id="5042", admin_id=admin_id)

def lambda_handler(event, context):

    # logging
    data = json.loads(event['body'])
    print(data)
    
    if data['topic'] == 'conversation.user.created':
        conversation_id = data['data']['item']['id']
        user_name = data['data']['item']['source']['author']['name']

        if is_work_hours():
          send_message_during_office_hours(conversation_id=conversation_id, admin_id=admin_id, user_name=user_name)
          send_alert_message(conversation_id=conversation_id, admin_id=admin_id, user_name=user_name)
        else:
            send_out_of_office_message(conversation_id=conversation_id, admin_id=admin_id, user_name=user_name)
            send_alert_message(conversation_id=conversation_id, admin_id=admin_id, user_name=user_name)
            snooze_conversation(conversation_id=conversation_id, admin_id=admin_id)
    return {
        'statusCode': 200,
        'body': json.dumps({'status': 'received'})
    }
