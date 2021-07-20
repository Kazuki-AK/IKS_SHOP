from django.urls import path
from . import views

app_name = 'Top'

urlpatterns = [
    path('', views.top, name='top'),
]
