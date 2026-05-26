from django.urls import path
from . import views

urlpatterns = [
    path("", views.inbox, name="inbox"),
    path("new/", views.send_message, name="new-message"),
    path("<int:pk>/", views.conversation_view, name="conversation"),
]
