from django.shortcuts import render, redirect
from django.http import HttpResponse
# contrib são apps que já vem instalados no Django
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth


def cadastro(request):
    if request.method == 'GET':
        # render() recebe dois parametros, request e o template
        return render(request, "cadastro.html")
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if senha != confirmar_senha:
            messages.add_message(request, constants.ERROR,
                                 "As senhas devem ser iguais")
            return redirect('/usuarios/cadastro')

        if len(senha) < 6:
            messages.add_message(request, constants.ERROR,
                                 "A senha deve conter mais de 6 dígitos")
            return redirect('/usuarios/cadastro')

        users = User.objects.filter(username=username)
        # exists() retorn True ou False se o usuário existe, ou não
        print(users.exists())

        if users.exists():
            messages.add_message(request, constants.ERROR,
                                 "Já existe um usuário com esse username")
            return redirect('/usuarios/cadastro')

        # o username à esquerda refere-se ao banco de dados, o username a direita refere-se ao valor que vc quer atribuir, ou seja, nesse exemplo refere-se ao username que veio do POST da url cadastro e está salvo na variável username
        user = User.objects.create_user(
            username=username,
            email=email,
            password=senha
        )

        return redirect('/usuarios/login')


def login(request):
    if request.method == 'GET':
        print(request.user)
        return render(request, 'login.html')
    elif request.method == 'POST':
        # username que está dentro do get() vem do template html
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        # verifica no banco de dados se existe um usuário com essas credenciais e retorna esse usuário para a variável user
        # se não existir, user recebe o valor None
        user = auth.authenticate(request, username=username, password=senha)

        if user:
            # armazena o usuário em sessão, atrela à requisição
            auth.login(request, user)
            return redirect('/pacientes/home')

        messages.add_message(request, constants.ERROR,
                             'Usuário ou senha inválidos')
        return redirect('/usuarios/login')


def logout(request):
    auth.logout(request)
    return redirect('/usuarios/login')
