from django.urls import path
from .views import delete_user, inbox, send_message

urlpatterns = [
    path('delete-account/', delete_user, name='delete_user'),
     path('inbox/', inbox, name='inbox'),
    path('send/', send_message, name='send_message'),
]
