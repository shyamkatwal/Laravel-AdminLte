from django.urls import path
from .views import showdata, dashboard, custom_query, account_view, accountdetails

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('showdata/', custom_query, name='showdata'),
    path('account/', account_view, name='account_view'),
    path('accountdetails/', accountdetails, name='accountdetails'),
]


