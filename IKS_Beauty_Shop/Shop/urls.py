from django.urls import path
from Shop.views import ShopView

app_name = 'Shop'

urlpatterns = [
    path('<int:pk>/', ShopView.as_view(), name='shop_info'),
]