from django.urls import path, include

urlpatterns = [
    path('addpost/', include('deeplink.urls'))
]