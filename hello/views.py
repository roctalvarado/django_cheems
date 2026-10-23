from django.shortcuts import render, redirect
from django.db import IntegrityError
from .entities.user import User
from .entities.log import Log
from .entities.ordenes import Ordenes
from .enums.profile import Profile
from hello.entities.order_history import OrderHistory

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
    if request.method == 'POST':
        if not request.session.get('user_id'):
            return redirect('login')

        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        status = request.POST.get('status', '1').strip()

        if title and description and status in ('1', '2', '3'):
            Ordenes.create(title, description, int(
                status), request.session['user_id'])
            return redirect('ordenes')

        error = 'Completa el título, la descripción y selecciona un estado.'
        return render(request, 'hello/ordenes.html', {
            'ordenes': Ordenes.get_all(),
            'error': error,
        })
    return render(request, 'hello/ordenes.html', {'ordenes': Ordenes.get_all()})


def login(request):

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


def historial_ordenes(request, id_user):
    user_orders = OrderHistory.get_by_user(id_user)
    with_user = next((u for u in User.get_all() if u.id == id_user), None)
    if with_user is None:
        return redirect('index')
    return render(request, 'hello/historial_ordenes.html', {
        'usuario': with_user,
        'historial': user_orders,
    })


def cambiar_estado(request, id_work_order):
    if not request.session.get('user_id'):
        return redirect('login')

    if request.method == 'POST':
        status = request.POST.get('status', '')
        if status in ('1', '2', '3'):
            Ordenes.change_status(id_work_order, int(
                status), request.session['user_id'])

    return redirect('ordenes')

def signup(request):
    if request.session.get('user_id'):
        return redirect('inicio')

    error = None
    name = ''
    account = ''

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        account = request.POST.get('account', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        if not name or not account or not password:
            error = 'Completa todos los campos.'
        elif len(name) > 45 or len(account) > 45:
            error = 'El nombre y la cuenta deben tener máximo 45 caracteres.'
        elif password != password2:
            error = 'Las contraseñas no coinciden.'
        else:
            try:
                User.create(name, account, password, Profile.OPERADOR)
                return redirect('/?registrado=1')
            except IntegrityError:
                error = 'Ya existe un usuario con esa cuenta.'

    return render(request, 'hello/signup.html', {
        'error': error,
        'name': name,
        'account': account,
    })
