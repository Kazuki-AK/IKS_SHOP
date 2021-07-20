from django.shortcuts import render
from django.views.generic import TemplateView

from UserLogin.models import *


# Create your views here.

class ShopView(TemplateView):
    template_name = 'shop/infomation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:

            shop_id = self.request.user.shop_number

            if Shop.objects.filter( pk = shop_id ).exists():
                context['shop'] = Shop.objects.get( pk = shop_id )
            else:
                pass
        else:
            pass
        return context