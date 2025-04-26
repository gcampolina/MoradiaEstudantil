from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from .forms import FotoPerfilForm

def home(request):
    return render(request,'home.html')

def sistema(request):
    usuario = request.user
    return render(request, 'sistema.html', {'usuario': usuario})


def login_view(request):
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Redirecione para a página desejada após o login
            return redirect('sistema')
        else:
            messages.error(request, 'Usuário ou senha inválido')
           
    
    return render(request, 'login.html')


def cadastro(request):
    if request.method == "POST":
        form_type = request.POST.get('form_type')
        
        # Cadastro de usuário
        if form_type == 'cadastro':
            username = request.POST.get('username')
            nome = request.POST.get('name')
            email = request.POST.get('email')
            senha = request.POST.get('password')
            confirmacao_senha = request.POST.get('password2')

            # Verificação de senhas
            if senha != confirmacao_senha:
                messages.warning(request, 'As senhas não coincidem.')
                return render(request, 'login.html', {
                'name': nome,
                'username': username,
                'email': email,
            })

            else:
                user = CustomUser.objects.filter(username=username).first()

                if user:
                    messages.warning(request, 'O usuário fornecido já está em uso.')
                    return render(request, 'login.html', {
                        'name': nome,
                        'username': username,
                        'email': email,
                    })

                else:
                    user = CustomUser.objects.create_user(username=username, email=email, password=senha)
                    user.first_name = nome
                    user.save()
                    messages.success(request, 'Cadastro efetuado com sucesso.')



    return render(request, 'login.html')


def conta(request):
    return render(request,'conta.html')

@login_required
def conta(request):
    if request.method == 'POST':
        form = FotoPerfilForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('conta')  # Redireciona para a mesma página para ver as mudanças
    else:
        form = FotoPerfilForm(instance=request.user)

    # Passe tanto o formulário quanto o usuário para o contexto
    context = {'form': form, 'usuario': request.user}
    return render(request, 'conta.html', context)