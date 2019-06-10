from django.urls import path
from .views import DeeplinkAdmitad, DeeplinkVigLink, SendPost

urlpatterns = [
    path('admitad/', DeeplinkAdmitad.as_view()),
    path('viglink/', DeeplinkVigLink.as_view()),
    path('admitad/send/', SendPost.as_view()),
    path('viglink/send/', SendPost.as_view()),
]