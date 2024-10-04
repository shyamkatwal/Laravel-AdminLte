from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('showdata/', custom_query, name='showdata'),
    #path('showdata/', showdata, name='showdata'),
]


