import json
import threading
from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer

from web.models import User, Message

lock = threading.Lock()
sockets = {}


class ChatConsumer(WebsocketConsumer):

    def websocket_connect(self, event):

        self.accept()

        params = self.scope['path'].split('/')

        dict_key = params[-1] + ":" + params[-2]

        try:
            lock.acquire()
            sockets.update({dict_key:self})
        finally:
            lock.release()
        print(sockets.items())
        print('connect', event)

    def websocket_receive(self, event):
        
        data = json.loads(event['text'])
        
        dict_key = data['receiver'] + ":" + data['sender']

        if dict_key in sockets.keys() :
          opponent = sockets.get(dict_key)
          opponent.send(event['text'])
        else :
            print("opponent is offline")

        sender = User.objects.get(username=data['sender'])
        receiver = User.objects.get(username=data['receiver'])
        message = Message(message=data['message'],sender=sender, receiver=receiver)
        message.save()

        print("on_message", event)


    def websocket_disconnect(self, event):
        
      params = self.scope['path'].split('/')

      dict_key = params[-1] + ":" + params[-2]

      try :
          lock.acquire()
          sockets.pop(dict_key)
      finally:
          lock.release()

      print("disconnect", event)
      print(sockets.items())
      raise StopConsumer()
