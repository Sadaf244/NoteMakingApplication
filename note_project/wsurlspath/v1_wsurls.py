from django.conf.urls import include
from django.urls import path

urlpatterns = [
    path('account/', include('ws.v1.account.wsurls')),
    path('notes/', include('ws.v1.user_note.wsurls')),
    ]
