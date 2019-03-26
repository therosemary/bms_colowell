from django.conf.urls import url

from projects import views

app_name = 'projects'
urlpatterns = [
    url(r'^ajax_salesman/$', views.ajax_salesman, name='ajax_salesman'),
    # url(r'^ajax_salesman/(?P<contract_number>.+)$', views.ajax_salesman, name='ajax_salesman'),

]
