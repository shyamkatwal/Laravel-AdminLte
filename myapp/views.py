from django.shortcuts import render
from .models import MyModel
from django.db import connection


# Create your views here.
def dashboard(request):
    return render(request, 'myapp/dashboard.html')

#def showdata(request):
    #records = MyModel.objects.all()
    #print(records.query)
    #return render(request, 'myapp/showdata.html', {'records': records})
    return render(request, 'myapp/showdata.html')

def custom_query(request):
    try:
       
        with connection.cursor() as cursor:
             query = "SELECT * FROM tbl_addressbook"
             cursor.execute(query)
             data = cursor.fetchall()
             return render(request, 'myapp/showdata.html', context={"records": data})
    except Exception as e:
        print(e)
        return render(request, 'myapp/error.html', context={"error": str(e)})
