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
import time
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, time, timedelta
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
            default = "Skype listener: Investigate if you see this."
            message = {"user_id":event.msg.userId,
                    "chat_id":event.msg.chatId,
                    "msg":event.msg.content}
            print(message)
            if('8:live:.cid.fb5d66f4c0a4f1c2' in event.msg.content):
                skype_obj = Skype(self.username, self.password, self.token_file)
                if('Hi' in event.msg.content):
                    channel = skype_obj.chats.chat(event.msg.chatId).sendMsg('Hi, This is task Bot')
                else:
                    channel = skype_obj.chats.chat(event.msg.chatId).sendMsg('Sorry, I don`t understand')

urlpatterns = [
    path('admin/', admin.site.urls),
]

skpyListner = SkypeListener()
# def runListner():
#     big_bro.loop()

# t1 = threading.Thread(target=runListner)
# t1.start()

# daily_Jobs = 

jobs = [
    {
        'job': 'shutdown',
        'hour': 6,
        'min': 30
    },
    {
        'job': 'start',
        'hour': 5,
        'min': 30
    },

    {
        'job': 'repeated',
        'channelId': '8:live:.cid.1c717c2c3e0bcdee',
        'msg': 'This is a schedule message, Please update your daily status',
        'hour': 5,
        'min': 30
    }
]

def schedule_job():
    # Create a scheduler object
    scheduler = BackgroundScheduler()

    # Set the timezone to IST
    ist = pytz.timezone('Asia/Kolkata')
    for obj in jobs:
        if(obj.get('job') in 'repeated'):
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
            scheduler.add_job(skpyListner.scheduleSender, 'date', run_date=target_datetime, args=(obj.get('channelId'), obj.get('msg')) )
        elif(obj.get('job') in 'shutdown'):
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
            scheduler.add_job(scheduler.shutdown, 'date', run_date=target_datetime)
        elif(obj.get('job') in 'start'):
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
            scheduler.add_job(main_thread_schdular, 'date', run_date=target_datetime)
    # Start the scheduler in a non-blocking manner
    scheduler.start()

def main_thread_schdular():
    main_thread_schdular = BackgroundScheduler()
    ist = pytz.timezone('Asia/Kolkata')
    # Define the time of day in IST when you want the job to run
    # For example, here we set it to 11:30 AM IST
    target_time = time(hour=3, minute=30)

    # Calculate the time difference between the current time and the target time in IST
    now = datetime.now(ist)
    target_datetime = ist.localize(datetime.combine(now.date(), target_time))
    time_difference = target_datetime - now

    # If the target time has already passed for today, schedule the job for the next day
    if time_difference.total_seconds() < 0:
        target_datetime += timedelta(days=1)

    # Schedule the job to run at the target_datetime in IST
    main_thread_schdular.add_job(schedule_job, 'date', run_date=target_datetime)

    # ======================================

    # Define the time of day in IST when you want the job to run
    # For example, here we set it to 11:30 AM IST
    target_time_destroy = time(hour=4, minute=30)

    # Calculate the time difference between the current time and the target time in IST
    now_destroy = datetime.now(ist)
    target_datetime_destroy = ist.localize(datetime.combine(now.date(), target_time_destroy))
    time_difference_destroy = target_datetime_destroy - now_destroy

    # If the target time has already passed for today, schedule the job for the next day
    if time_difference_destroy.total_seconds() < 0:
        target_datetime_destroy += timedelta(days=1)

    #==================================
    # Job to destroy it's own instance
    main_thread_schdular.add_job(main_thread_schdular.shutdown, 'date', run_date=target_datetime_destroy)

    main_thread_schdular.start()


main_thread_schdular()