from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/messanger/(?P<pk>\d+)/$', consumers.ChatConsumer.as_asgi()),
]