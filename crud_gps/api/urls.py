from django.urls import path
from .views import PosicionView

urlpatterns = [
    path('posicion/', PosicionView.as_view(), name='posicion_list'),
    path('posicion/<int:posicion_id>/', PosicionView.as_view(), name='posicion_detail'),
]
