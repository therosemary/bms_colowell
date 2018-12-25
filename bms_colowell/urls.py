from bms_colowell.admin_bms_colowell import BMS_admin_site
from django.urls import include, path


urlpatterns = [
    path('admin/', BMS_admin_site.urls),
    
    path('cas/', include(("mama_cas.urls", "mama_cas"), namespace="mama_cas")),
    
    path('accounts/', include(("accounts.urls", "accounts"), namespace="accounts")),
    path('partners/', include(("partners.urls", "partners"), namespace="partners")),
    path('products/', include(("products.urls", "products"), namespace="products")),
]
