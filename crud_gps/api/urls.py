from django.urls import path
from .views import PosicionView, ExportToExcelView

urlpatterns = [
    path('posicion/', PosicionView.as_view(), name='posicion_list'),
    path('posicion/<int:posicion_id>/', PosicionView.as_view(), name='posicion_detail'),
    path('export-excel/', ExportToExcelView.as_view(), name='export_excel'),
]
