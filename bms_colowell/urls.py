from django.urls import include, path

from django_cas_ng import views as cas_client_views

from bms_colowell.admin_bms_colowell import BMS_admin_site
from bms_colowell.views import dingtalk_auth


urlpatterns = [
    # admin authentications
    path('', BMS_admin_site.urls),

    # cas authentications
    path('cas/login', cas_client_views.LoginView.as_view(), name='cas_ng_login'),
    path('cas/logout', cas_client_views.LogoutView.as_view(), name='cas_ng_logout'),
    path('cas/callback', cas_client_views.CallbackView.as_view(), name='cas_ng_proxy_callback'),
    
    # dingtalk authentications
    path('dingtalk_auth/', dingtalk_auth),
    
    path('accounts/', include(("accounts.urls", "accounts"), namespace="accounts")),
    path('partners/', include(("partners.urls", "partners"), namespace="partners")),
    path('products/', include(("products.urls", "products"), namespace="products")),
]
