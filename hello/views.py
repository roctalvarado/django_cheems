from django.shortcuts import render
from .entities.user import User
from .entities.log import Log
from hello.entities import user
from .entities.ordenes import Ordenes

# Create your views here.
def display(request):
    return render(request, 'hello/display.html')

def index(request):
    users = User.get_all()
    return render(request, 'hello/index.html', {'users': users})

def logs(request):
    logs = Log.get_all()
    return render(request, 'hello/logs.html', {'logs': logs})





def lista_ordenes(request):
    ordenes = Ordenes.get_all()
    return render(request, 'hello/ordenes.html', {'ordenes': ordenes})
