from django.shortcuts import render
from .models import MyModel
from django.db import connection


# Create your views here.
def dashboard(request):
    return render(request, 'myapp/dashboard.html')

def showdata(request):
    records = MyModel.objects.all()
    print(records.query)
    #return render(request, 'myapp/showdata.html', {'records': records})

def custom_query(request):
    try:
        query = "SELECT * FROM finfadm.urm_upr_coreserver"
        with connection.cursor() as cursor:
            queryset = cursor.execute(query)
            data = queryset.fetchall()
            return render(request, 'myapp/showdata.html', context={"records": data})

    except Exception as e:
        print(e)
