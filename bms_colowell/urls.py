from bms_colowell.admin_bms_colowell import BMS_admin_site
from django.urls import include, path


urlpatterns = [
    path('admin/', BMS_admin_site.urls),
    path('accounts/', include(("accounts.urls", "accounts"), namespace="accounts")),
    path('products/', include(("products.urls", "products"), namespace="products")),
]
