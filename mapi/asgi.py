# """
# ASGI config for mapi project.
#
# It exposes the ASGI callable as a module-level variable named ``application``.
#
# For more information on this file, see
# https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
# """
#
import os
from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.sessions import SessionMiddlewareStack
# from orders.routing import websocket_urlpatterns
#
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mapi.settings')
#
# django_asgi_app = get_asgi_application()
# application = ProtocolTypeRouter({
#     "http": django_asgi_app,
#     "websocket": SessionMiddlewareStack(
#         URLRouter(
#             websocket_urlpatterns
#         )
#     )
# })
application = get_asgi_application()