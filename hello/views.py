from django.shortcuts import render
from .entities.user import User
from .entities.log import Log

# Create your views here.
def index(request):
    users = User.get_all()
    return render(request, 'hello/index.html', {'users': users})

def logs(request):
    logs = Log.get_all()
    return render(request, 'hello/logs.html', {'logs': logs})
