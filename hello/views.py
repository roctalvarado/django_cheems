from django.shortcuts import render, redirect
from .entities.user import User
from .entities.log import Log
from hello.entities import user
from .entities.ordenes import Ordenes

# Create your views here.
def display(request):
    if not request.session.get('user_id'):
        return redirect('login')
    return render(request, 'hello/display.html')

def index(request):
    users = User.get_all()
    return render(request, 'hello/index.html', {'users': users})

def logs(request):
    logs = Log.get_all()
    return render(request, 'hello/logs.html', {'logs': logs})

def ordenes(request):
    ordenes = Ordenes.get_all()
    return render(request, 'hello/ordenes.html', {'ordenes': ordenes})

def login(request):
    if request.session.get('user_id'):
        return redirect('inicio')

    error = None
    account = ''

    if request.method == 'POST':
        account = request.POST.get('account', '').strip()
        password = request.POST.get('password', '')

        if not account or not password:
            error = 'Escribe tu cuenta y tu contraseña'
        else:
            user = User.authenticate(account, password)
            if user:
                request.session['user_id'] = user['id']
                request.session['user_name'] = user['name']
                request.session['user_profile'] = user['profile']
                return redirect('inicio')
            error = 'Cuenta o contraseña incorrectas'

    return render(request, 'hello/login.html', {'error': error, 'account': account})

def logout(request):
    request.session.flush()
    return redirect('login')