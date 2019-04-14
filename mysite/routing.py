from django.conf.urls import url
from django.urls import path,re_path
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator,OriginValidator

from chat.consumers import ChatConsumer

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket':AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    re_path(r"^messages/(?P<username>[\w+@+-]+)", ChatConsumer)
                    #path('messages',ChatConsumer)
                    #url(r"^$",ChatConsumer)
                ]
            )
        )
    )
})


#ws://ourdomain/