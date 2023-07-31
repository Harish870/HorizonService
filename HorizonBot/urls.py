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
import threading
from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from skpy import SkypeEventLoop, SkypeNewMessageEvent, Skype
class SkypeListener(SkypeEventLoop):
    username = 'taskBot3.0@gmail.com'
    password = 'taskBot@3'
    token_file = '.tokens-app'
    "Listen to a channel continuously"
    def __init__(self):
        super(SkypeListener, self).__init__(self.username, self.password, self.token_file)
 
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
                    #channel.sendMsg('Hi, this is automated test message "Please update daily status"')

urlpatterns = [
    path('admin/', admin.site.urls),
]

big_bro = SkypeListener()
def runListner():
    big_bro.loop()

t1 = threading.Thread(target=runListner)

t1.start()
