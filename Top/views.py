from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

# Create your views here.

def top(request):
  template_name = "top.html"
  return render(request,template_name)