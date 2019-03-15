from django.urls import path

from suggestions.views import report_view


urlpatterns = [
    path('report/<int:user_id>/<str:barcode>/<str:token>/', report_view, name='report'),
]
