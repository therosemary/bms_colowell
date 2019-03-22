from django.urls import path

from lz_products.views import lz_report_view, batch_download


urlpatterns = [
    path('report/<int:user_id>/<str:barcode>/<str:token>/',
         lz_report_view, name='lz_report'),
    path('batch_download/<int:user_id>/<str:serial_number>/<str:token>/',
         batch_download, name='batch_download'),
]
