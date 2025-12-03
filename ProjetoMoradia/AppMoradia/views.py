from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .forms import FotoPerfilForm
from .models import CustomUser, Enquete, Voto, Aviso

def home(request):
    return render(request, 'home.html')

@login_required
def sistema(request):
    usuario = request.user
    return render(request, 'sistema.html', {'usuario': usuario})


def suporte(request):
    usuario = request.user
    usuarios = CustomUser.objects.all()
    return render(request, 'suporte.html', {'usuario': usuario, 'usuarios': usuarios})


@login_required
def dashboard(request):
    enquetes_ativas = Enquete.objects.filter(status='ATIVA').count()

    try:
        ultimo_aviso = Aviso.objects.latest('data_criacao')
        ultimo_aviso_titulo = ultimo_aviso.titulo
        ultimo_aviso_descricao = ultimo_aviso.descricao
        ultimo_aviso_data_criacao = ultimo_aviso.data_criacao
        ultimo_aviso_criado_por = ultimo_aviso.criado_por.first_name if ultimo_aviso.criado_por else "Desconhecido"
    except Aviso.DoesNotExist:
        ultimo_aviso_titulo = "Nenhum aviso no momento"
        ultimo_aviso_descricao = ""
        ultimo_aviso_data_criacao = ""
        ultimo_aviso_criado_por = ""

    # Dados para o painel principal
    return render(request, 'sistema.html', {
        'usuario': request.user,
        'ultimo_aviso_titulo': ultimo_aviso_titulo,
        'ultimo_aviso_descricao': ultimo_aviso_descricao,
        'ultimo_aviso_criado_por': ultimo_aviso_criado_por,
        'ultimo_aviso_data_criacao': ultimo_aviso_data_criacao,
        'enquetes_ativas': enquetes_ativas,
    })


@login_required
def enquetes(request):
    enquetes_ativas = Enquete.objects.filter(status='ATIVA').order_by('-data_criacao')
    enquetes_encerradas = Enquete.objects.filter(status='ENCERRADA').order_by('-data_criacao')
    usuario = request.user

    for enquete in enquetes_ativas:
        enquete.votos_sim = enquete.votos.filter(escolha='SIM').count()
        enquete.votos_nao = enquete.votos.filter(escolha='NÇŸO').count()
        enquete.usuarios_sim = enquete.votos.filter(escolha='SIM').select_related('usuario')
        enquete.usuarios_nao = enquete.votos.filter(escolha='NÇŸO').select_related('usuario')

    for enquete in enquetes_encerradas:
        enquete.votos_sim = enquete.votos.filter(escolha='SIM').count()
        enquete.votos_nao = enquete.votos.filter(escolha='NÇŸO').count()

    return render(request, 'enquetes.html', {
        'enquetes_ativas': enquetes_ativas,
        'enquetes_encerradas': enquetes_encerradas,
        'usuario': usuario,
    })


@login_required
def criar_enquete(request):
    if request.method == 'POST':
        pergunta = request.POST['pergunta']
        Enquete.objects.create(
            pergunta=pergunta,
            criado_por=request.user
        )
        messages.success(request, 'Enquete criada com sucesso!')
        return redirect('enquetes')


@login_required
def excluir_enquete(request, enquete_id):
    enquete = get_object_or_404(Enquete, id=enquete_id)
    if request.user == enquete.criado_por or request.user.tipo == 'COORDENADOR':
        enquete.delete()
        messages.success(request, 'Enquete excluida com sucesso!')
    else:
        messages.error(request, 'Voce nao tem permissao para excluir esta enquete.')
    return redirect('enquetes')

@login_required
def votar_enquete(request, enquete_id):
    enquete = get_object_or_404(Enquete, id=enquete_id)

    if request.method == 'POST':
        escolha = request.POST.get('escolha')  # 'SIM' ou 'NAO'

        if escolha in ['SIM', 'NÇŸO']:
            voto, _ = Voto.objects.get_or_create(enquete=enquete, usuario=request.user)
            voto.escolha = escolha
            voto.save()

        return redirect('enquetes')

    return redirect('enquetes')

def resultados_enquete(request, enquete_id):
    enquete = get_object_or_404(Enquete, id=enquete_id)

    votos_sim = enquete.votos.filter(escolha='SIM').count()
    votos_nao = enquete.votos.filter(escolha='NÇŸO').count()

    return render(request, 'enquetes.html', {
        'enquete': enquete,
        'votos_sim': votos_sim,
        'votos_nao': votos_nao
    })

def detalhes_enquete(request, enquete_id):
    try:
        votos = Voto.objects.filter(enquete_id=enquete_id)

        votos_sim = [voto.usuario.get_full_name() or voto.usuario.username for voto in votos.filter(escolha='SIM')]
        votos_nao = [voto.usuario.get_full_name() or voto.usuario.username for voto in votos.filter(escolha='NÇŸO')]

        return JsonResponse({
            'sim': list(votos_sim),
            'nao': list(votos_nao),
        })
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)

@login_required
def encerrar_enquete(request, enquete_id):
    enquete = get_object_or_404(Enquete, id=enquete_id)
    if request.user == enquete.criado_por or request.user.tipo == 'COORDENADOR':
        enquete.status = 'ENCERRADA'
        enquete.data_encerramento = timezone.now()
        enquete.save()
        messages.success(request, 'Enquete encerrada com sucesso!')
    else:
        messages.error(request, 'Voce nao tem permissao para encerrar esta enquete.')
    return redirect('enquetes')

@login_required
def avisos(request):
    usuario = request.user
    avisos = Aviso.objects.all().order_by('-data_criacao')
    return render(request, 'avisos.html', {'usuario': usuario, 'avisos': avisos})

@login_required
def adicionar_aviso(request):
    if request.user.tipo not in ['SÇ?NDICO', 'COORDENADOR']:
        messages.error(request, 'Voce nao tem permissao para adicionar avisos.')
        return redirect('avisos')

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')

        Aviso.objects.create(titulo=titulo, descricao=descricao, criado_por=request.user)
        messages.success(request, 'Aviso adicionado com sucesso!')
        return redirect('avisos')

    return render(request, 'adicionar_aviso.html', {'usuario': request.user})

@login_required
def excluir_aviso(request, aviso_id):
    aviso = get_object_or_404(Aviso, id=aviso_id)

    if request.user.tipo == 'COORDENADOR':
        aviso.delete()  # Coordenador pode excluir qualquer aviso
        messages.success(request, 'Aviso excluido com sucesso!')
    elif request.user.tipo == 'SÇ?NDICO' and aviso.criado_por == request.user:
        aviso.delete()  # Sindico so pode excluir seu proprio aviso
        messages.success(request, 'Aviso excluido com sucesso!')
    else:
        messages.error(request, 'Voce nao tem permissao para excluir este aviso.')

    return redirect('avisos')


@login_required
def painelcontrole(request):
    if request.user.tipo != 'COORDENADOR':
        messages.error(request, 'Voce nao tem permissao para acessar essa pagina.')
        return redirect('sistema')
    
    usuario = request.user
    usuarios = CustomUser.objects.all()
    return render(request,'painel-controle.html', {'usuario': usuario, 'usuarios': usuarios,})

    

@login_required
def update_user(request, user_id):
    if request.user.tipo != 'COORDENADOR':
        messages.error(request, 'Voce nao tem permissao.')
    
    
    user = get_object_or_404(CustomUser, id=user_id)
    user.first_name = request.POST.get('nome')  
    user.username = request.POST.get('username')  
    user.email = request.POST.get('email')
    user.telefone = request.POST.get('telefone') 
    user.tipo = request.POST.get('tipo')
    user.save()
    messages.success(request, f'Usuario {user.username} atualizado com sucesso!')
    return redirect('painel-controle')




@login_required
def delete_user(request, user_id):
    if request.user.tipo != 'COORDENADOR':
        messages.error(request, 'Voce nao tem permissao.')
    
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    messages.success(request, f'Usuario {user.username} excluido com sucesso!')
    return redirect('painel-controle')
    

    

def login_view(request):
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user:
            if user.tipo == 'VISITANTE':
                messages.warning(request, 'Aguardando aprovacao do coordenador para acessar o sistema.')
                return redirect('login')
            else:
                login(request, user)
                return redirect('sistema')
        else:
            messages.error(request, 'Usuario ou senha invalido')
           
    
    return render(request, 'login.html')


def cadastro(request):
    if request.method == "POST":
        form_type = request.POST.get('form_type')
        
        if form_type == 'cadastro':
            username = request.POST.get('username')
            nome = request.POST.get('name')
            email = request.POST.get('email')
            senha = request.POST.get('password')
            confirmacao_senha = request.POST.get('password2')
            telefone = request.POST.get('telefone', '').replace('(', '').replace(')', '').replace(' ', '').replace('-', '')

            if senha != confirmacao_senha:
                messages.warning(request, 'As senhas nao coincidem.')
                return render(request, 'login.html', {
                'name': nome,
                'username': username,
                'email': email,
            })

            else:
                user = CustomUser.objects.filter(username=username).first()

                if user:
                    messages.warning(request, 'O usuario fornecido ja esta em uso')
                    return render(request, 'login.html', {
                        'name': nome,
                        'username': username,
                        'email': email,
                    })

                else:
                    user = CustomUser.objects.create_user(username=username, email=email, password=senha, telefone=telefone)
                    user.first_name = nome
                    user.save()
                    messages.success(request, 'Cadastro efetuado com sucesso!')



    return render(request, 'login.html')



@login_required
def conta(request):
    if request.method == 'POST':
        form = FotoPerfilForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('conta')
    else:
        form = FotoPerfilForm(instance=request.user)

    context = {'form': form, 'usuario': request.user}
    return render(request, 'conta.html', context)


