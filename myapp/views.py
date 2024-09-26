from django.shortcuts import render


# Create your views here.
def dashboard(request):
    return render(request, 'myapp/dashboard.html')

def showdata(request):
    return render(request, 'showdata.html')
