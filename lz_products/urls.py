from django.urls import path

from lz_products.views import lz_report_view


urlpatterns = [
    path('report/<int:user_id>/<str:barcode>/<str:token>/',
         lz_report_view, name='lz_report'),
]
