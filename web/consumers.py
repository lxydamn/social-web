import json
from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer

from web.models import User, Message


class ChatConsumer(WebsocketConsumer):
  def websocket_connect(self, event):
      self.accept()
      print('connect', event)

  def websocket_receive(self, event):
    print("on_message", event)
    
   
  def websocket_disconnect(self, event):
    print("disconnect", event)
    raise StopConsumer()
    


