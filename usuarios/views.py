from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib import messages, auth
from .models import Users as User

def login(request):
    if request.user.is_authenticated:
        return redirect('/plataforma/home')
    status = request.GET.get('status')
    return render(request, 'login.html', {'status': status})

def cadastro(request):
    if request.user.is_authenticated:
        return redirect('/plataforma/home')
    status = request.GET.get('status')
    return render(request, 'cadastro.html', {'status': status})

def valida_cadastro(request):
    nome = request.POST.get('nome')
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    cep = request.POST.get('cep')
    rua = request.POST.get('rua')
    numero = request.POST.get('numero')

    if len(nome.strip()) == 0 or len(email.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Nome e email não podem estar vazios')
        return redirect('/auth/cadastro/')

    if len(senha) < 8:
        messages.add_message(request, constants.ERROR, 'Sua senha deve ter no minino 8 digitos ')
        return redirect('/auth/cadastro/')

    if User.objects.filter(email = email).exists():
        messages.add_message(request, constants.ERROR, 'Email já Cadastrado')
        return redirect('/auth/cadastro/')
    
    if User.objects.filter(username = nome).exists():
        messages.add_message(request, constants.ERROR, 'Já existe esse usuario com esse nome')
        return redirect('/auth/cadastro/')

    try:
        usuario = User.objects.create_user(username = nome, email = email, password = senha, rua=rua, numero=numero, cep=cep)
        usuario.save()

        messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com Sucesso!')
        return redirect('/auth/cadastro/')
    except:
        messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
        return redirect('/auth/cadastro/')


def valida_login(request):
    nome = request.POST.get('nome')
    senha = request.POST.get('senha')

    usuario = auth.authenticate(username = nome, password = senha)
    print(usuario)
    
    if not usuario:
        messages.add_message(request, constants.ERROR, 'Email ou senha inválidos')
        return redirect('/auth/login/')
    else:
        auth.login(request, usuario)
        return redirect('/plataforma/home')


def sair(request):
    auth.logout(request)
    messages.add_message(request, constants.WARNING, 'Faça um login antes de acessar o sistema')
    return redirect('/auth/login/')