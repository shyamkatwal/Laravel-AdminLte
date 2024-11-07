from django.urls import path
from .views import showdata, dashboard, custom_query, account_view, account_details

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('showdata/', custom_query, name='showdata'),
    path('account/', account_view, name='account_view'),
    path('account_details/', account_details, name='account_details'),
]


