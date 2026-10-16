from django.shortcuts import render
from .entities.user import User
from .entities.ordenes import Ordenes

# Create your views here.
def index(request):
    users = User.get_all()
    return render(request, 'hello/index.html', {'users': users})




def lista_ordenes(request):
    ordenes = Ordenes.get_all()
    return render(request, 'hello/ordenes.html', {'ordenes': ordenes})