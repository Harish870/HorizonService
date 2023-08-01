"""
URL configuration for HorizonBot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
    
"""
from datetime import datetime, timedelta
import threading
from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from skpy import SkypeEventLoop, SkypeNewMessageEvent, Skype
import schedule
import pytz
import time as t
import re
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, time, timedelta
import pymongo
client = pymongo.MongoClient('mongodb+srv://horizonPPD:aRBbTQMBAJiqkmEk@cluster0.hho8d6f.mongodb.net/?retryWrites=true&w=majority')
#Define Db Name
dbname = client['ppd-horizon']

#Define Collection
collection = dbname['ppd-job-data']

main_thread_schdular = BackgroundScheduler()
class SkypeListener(SkypeEventLoop):
    username = 'taskBot3.0@gmail.com'
    password = 'taskBot@3'
    token_file = '.tokens-app'
    "Listen to a channel continuously"
    def __init__(self):
        super(SkypeListener, self).__init__(self.username, self.password, self.token_file)
 
    def scheduleSender(self, chat_Id, msg):
        skype_obj = Skype(self.username, self.password, self.token_file)
        channel = skype_obj.chats.chat(chat_Id).sendMsg(msg)

    def onEvent(self, event):
        if isinstance(event, SkypeNewMessageEvent):
            pattern = r'set reminder msg="([^"]+)",\s*hour="(\d+)",\s*min="(\d+)"\s+and\s+repeatition_type="([^"]+)"'
            match = re.search(pattern, event.msg.content.replace('&quot;', '"'), re.IGNORECASE)
            if('8:live:.cid.fb5d66f4c0a4f1c2' in event.msg.content):
                skype_obj = Skype(self.username, self.password, self.token_file)
                if(any(word in event.msg.content.lower() for word in ["hi", "hello", "hey"])):
                    channel = skype_obj.chats.chat(event.msg.chatId).sendMsg('Hi, This is task Bot')
                elif('what can you do' in event.msg.content.lower()) :
                    channel = skype_obj.chats.chat(event.msg.chatId).sendMsg('I can set reminders for you - just write "set reminder msg="Example Message", hour="", min="" and repeation_type="repeated/once"')
                elif(match):
                    example_message = match.group(1)
                    hour = int(match.group(2))
                    minute = int(match.group(3))
                    repetition_type = match.group(4)
                    schdule_ist_job(event.msg.chatId, example_message, hour, minute)
                    if(repetition_type in "repeated"):
                        collection.insert(
                            {
                            "job": repetition_type,
                            "channelId": event.msg.chatId,
                            "msg": example_message,
                            "hour": int(hour),
                            "min": int(minute)
                            }
                        )
                    skype_obj.chats.chat(event.msg.chatId).sendMsg(f"example_message={example_message}, hour={hour}, minute={minute}, repetion_type={repetition_type}")

skpyListner = SkypeListener()

def schdule_ist_job(id, msg, hour, min):
    # Define the time of day in IST when you want the job to run
    # For example, here we set it to 11:30 AM IST
    ist = pytz.timezone('Asia/Kolkata')
    target_time = time(hour=hour, minute=min)

    # Calculate the time difference between the current time and the target time in IST
    now = datetime.now(ist)
    target_datetime = ist.localize(datetime.combine(now.date(), target_time))
    time_difference = target_datetime - now

    # If the target time has already passed for today, schedule the job for the next day
    if time_difference.total_seconds() < 0:
        target_datetime += timedelta(days=1)
    print("In this fun")
    # Schedule the job to run at the target_datetime in IST
    main_thread_schdular.add_job(skpyListner.scheduleSender, 'date', run_date=target_datetime, args=(id, msg) )


urlpatterns = [
    path('admin/', admin.site.urls),
]
def runListner():
    skpyListner.loop()

t1 = threading.Thread(target=runListner)
t1.start()


def schedule_job():
    jobs = []
    data = collection.find({})

    for r in data:
        jobs.append(r)
    main_thread_schdular.remove_all_jobs()
    # Set the timezone to IST
    ist = pytz.timezone('Asia/Kolkata')
    print('In Schdule')
    for obj in jobs:
        if(obj.get('job') in 'repeated'):
            print('In repeated')
            # Define the time of day in IST when you want the job to run
            # For example, here we set it to 11:30 AM IST
            target_time = time(hour=obj.get('hour'), minute=obj.get('min'))

            # Calculate the time difference between the current time and the target time in IST
            now = datetime.now(ist)
            target_datetime = ist.localize(datetime.combine(now.date(), target_time))
            time_difference = target_datetime - now

            # If the target time has already passed for today, schedule the job for the next day
            if time_difference.total_seconds() < 0:
                target_datetime += timedelta(days=1)

            # Schedule the job to run at the target_datetime in IST
            main_thread_schdular.add_job(skpyListner.scheduleSender, 'date', run_date=target_datetime, args=(obj.get('channelId'), obj.get('msg')) )

def main_thread_schdular_fun():
    # Create a BackgroundScheduler instance

    # Set the system's timezone to IST
    ist_timezone = pytz.timezone('Asia/Kolkata')
    datetime_ist = datetime.now(ist_timezone)

    # Calculate the initial delay to the desired time in IST
    target_time = time(10, 00, 0)  # 8:00 AM IST
    target_datetime = ist_timezone.localize(datetime(datetime_ist.year, datetime_ist.month, datetime_ist.day, target_time.hour, target_time.minute, target_time.second))

    print(target_datetime, 'target date time')
    # Add a job to the scheduler
    main_thread_schdular.add_job(schedule_job, trigger='interval', seconds=24 * 60 * 60, start_date=target_datetime, timezone=ist_timezone)

    # Start the scheduler
    main_thread_schdular.start()


main_thread_schdular_fun()