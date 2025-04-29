from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from .forms import FotoPerfilForm
from .models import CustomUser, Evento, Enquete, Voto
from django.utils import timezone
from datetime import date
from .models import Aviso

def home(request):
    return render(request,'home.html')


@login_required
def sistema(request):
    usuario = request.user
    return render(request, 'sistema.html', {'usuario': usuario})


@login_required
def dashboard(request):
    hoje = timezone.now().date()  # Pega a data de hoje
    # Filtra os eventos que ocorrerão hoje ou no futuro
    eventos_futuros = Evento.objects.filter(data__gte=hoje).order_by('data') # Pega o primeiro evento com data maior ou igual a hoje
    enquetes_ativas = Enquete.objects.filter(status='ATIVA').count()

    
    # Se não houver evento, definimos uma variável default
    if eventos_futuros.exists():
        evento_proximo = eventos_futuros.first()
        evento_proximo_titulo = evento_proximo.titulo
        evento_proximo_descricao = evento_proximo.descricao
        evento_proximo_data = evento_proximo.data.strftime('%d/%m/%Y')  # Formata a data
        evento_proximo_criado_por = evento_proximo.criado_por.first_name if evento_proximo.criado_por else "Desconhecido"
    else:
        evento_proximo_titulo = "Nenhum evento futuro."
        evento_proximo_data = "N/A"

    try:
        ultimo_aviso = Aviso.objects.latest('data_criacao')
        ultimo_aviso_titulo = ultimo_aviso.titulo
        ultimo_aviso_descricao = ultimo_aviso.descricao
        ultimo_aviso_data_criacao = ultimo_aviso.data_criacao
        ultimo_aviso_criado_por = ultimo_aviso.criado_por.first_name if ultimo_aviso.criado_por else "Desconhecido"
    except Aviso.DoesNotExist:
        ultimo_aviso_titulo = "Nenhum aviso no momento."


    # Passa a lista de eventos e o próximo evento para o template
    return render(request, 'sistema.html', {
        'usuario': request.user,
        'evento_proximo_titulo': evento_proximo_titulo,
        'evento_proximo_data': evento_proximo_data,
        'eventos_futuros': eventos_futuros,
        'evento_proximo_descricao' : evento_proximo_descricao,
        'evento_proximo_criado_por' : evento_proximo_criado_por,
        'ultimo_aviso_titulo': ultimo_aviso_titulo,
        'ultimo_aviso_descricao' : ultimo_aviso_descricao,
        'ultimo_aviso_criado_por' : ultimo_aviso_criado_por,
        'ultimo_aviso_data_criacao' : ultimo_aviso_data_criacao,
        'enquetes_ativas': enquetes_ativas,
    })




@login_required
def enquetes(request):
    enquetes_ativas = Enquete.objects.filter(status='ATIVA').order_by('-data_criacao')
    enquetes_encerradas = Enquete.objects.filter(status='ENCERRADA').order_by('-data_criacao')
    usuario = request.user

    for enquete in enquetes_ativas:
        enquete.votos_sim = enquete.votos.filter(escolha='SIM').count()
        enquete.votos_nao = enquete.votos.filter(escolha='NÃO').count()
        enquete.usuarios_sim = enquete.votos.filter(escolha='SIM').select_related('usuario')
        enquete.usuarios_nao = enquete.votos.filter(escolha='NÃO').select_related('usuario')

    for enquete in enquetes_encerradas:
        enquete.votos_sim = enquete.votos.filter(escolha='SIM').count()
        enquete.votos_nao = enquete.votos.filter(escolha='NÃO').count()

    return render(request, 'enquetes.html', {'enquetes_ativas': enquetes_ativas, 'enquetes_encerradas' : enquetes_encerradas, 'usuario': usuario})


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
        messages.success(request, 'Enquete excluída com sucesso!')
    else:
        messages.error(request, 'Você não tem permissão para excluir esta enquete.')
    return redirect('enquetes')

@login_required
def votar_enquete(request, enquete_id):
    enquete = get_object_or_404(Enquete, id=enquete_id)

    if request.method == 'POST':
        escolha = request.POST.get('escolha')  # 'SIM' ou 'NÃO'

        if escolha in ['SIM', 'NÃO']:
            voto, created = Voto.objects.get_or_create(enquete=enquete, usuario=request.user)
            voto.escolha = escolha
            voto.save()

        return redirect('enquetes')  # ou outra URL de destino

    return redirect('enquetes')

def resultados_enquete(request, enquete_id):
    enquete = get_object_or_404(Enquete, id=enquete_id)

    # Contagem de votos "Sim" e "Não"
    votos_sim = enquete.votos.filter(escolha='SIM').count()
    votos_nao = enquete.votos.filter(escolha='NÃO').count()

    return render(request, 'enquetes.html', {
        'enquete': enquete,
        'votos_sim': votos_sim,
        'votos_nao': votos_nao
    })

def detalhes_enquete(request, enquete_id):
    try:
        votos = Voto.objects.filter(enquete_id=enquete_id)

        votos_sim = [voto.usuario.get_full_name() or voto.usuario.username for voto in votos.filter(escolha='SIM')]
        votos_nao = [voto.usuario.get_full_name() or voto.usuario.username for voto in votos.filter(escolha='NÃO')]

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
        messages.error(request, 'Você não tem permissão para encerrar esta enquete.')
    return redirect('enquetes')

@login_required
def avisos(request):
    usuario = request.user
    avisos = Aviso.objects.all().order_by('-data_criacao') 
    return render(request, 'avisos.html', {'usuario': usuario, 'avisos': avisos})

@login_required
def adicionar_aviso(request):
    if request.user.tipo not in ['SÍNDICO', 'COORDENADOR']:
        messages.error(request, 'Você não tem permissão para adicionar avisos.')
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
        messages.success(request, 'Aviso excluído com sucesso!')
    elif request.user.tipo == 'SÍNDICO' and aviso.criado_por == request.user:
        aviso.delete()  # Síndico só pode excluir seu próprio aviso
        messages.success(request, 'Aviso excluído com sucesso!')
    else:
        messages.error(request, 'Você não tem permissão para excluir este aviso.')

    return redirect('avisos')


@login_required
def eventos(request):
    usuario = request.user
    hoje = date.today()
    eventos = Evento.objects.all()
    return render(request, 'eventos.html', {'usuario': usuario, 'eventos': eventos, 'hoje': hoje})


@login_required
def adicionar_evento(request):
    if request.user.tipo not in ['SÍNDICO', 'COORDENADOR']:
        messages.error(request, 'Você não tem permissão para adicionar eventos.')
        return redirect('eventos')

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        data = request.POST.get('data')

        Evento.objects.create(titulo=titulo, descricao=descricao, data=data, criado_por=request.user)
        messages.success(request, 'Evento adicionado com sucesso!')
        return redirect('eventos')

    return render(request, 'adicionar_evento.html', {'usuario': request.user})


@login_required
def excluir_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    
    # Verificar se o usuário tem permissão para excluir o evento
    if request.user.tipo == 'COORDENADOR':
        evento.delete()  # Coordenador pode excluir qualquer evento
        messages.success(request, 'Evento excluído com sucesso!')
    elif request.user.tipo == 'SÍNDICO' and evento.criado_por == request.user:
        evento.delete()  # Síndico só pode excluir seu próprio evento
        messages.success(request, 'Evento excluído com sucesso!')
    else:
        messages.error(request, 'Você não tem permissão para excluir este evento.')
    
    return redirect('eventos')  # Redireciona para o dashboard




@login_required
def painelcontrole(request):
    if request.user.tipo != 'COORDENADOR':
        messages.error(request, 'Você não tem permissão para acessar essa página.')
        return redirect('sistema')
    
    usuario = request.user
    usuarios = CustomUser.objects.all()
    return render(request,'painel-controle.html', {'usuario': usuario, 'usuarios': usuarios,})

    

@login_required
def update_user(request, user_id):
    if request.user.tipo != 'COORDENADOR':
        messages.error(request, 'Você não tem permissão.')
    
    
    user = get_object_or_404(CustomUser, id=user_id)
    user.first_name = request.POST.get('nome')  
    user.username = request.POST.get('username')  
    user.email = request.POST.get('email') 
    user.tipo = request.POST.get('tipo')
    user.save()
    messages.success(request, f'Usuário {user.username} atualizado com sucesso!')
    return redirect('painel-controle')




@login_required
def delete_user(request, user_id):
    if request.user.tipo != 'COORDENADOR':
        messages.error(request, 'Você não tem permissão.')
    
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    messages.success(request, f'Usuário {user.username} excluído com sucesso!')
    return redirect('painel-controle')
    

    

def login_view(request):
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user:
            if user.tipo == 'VISITANTE':
                messages.warning(request, 'Aguardando aprovação do coordenador para acessar o sistema.')
                return redirect('login')  # volta pra página de login
            else:
                login(request, user)
                return redirect('sistema')  # ou para onde você quiser
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
                    messages.warning(request, 'O usuário fornecido já está em uso')
                    return render(request, 'login.html', {
                        'name': nome,
                        'username': username,
                        'email': email,
                    })

                else:
                    user = CustomUser.objects.create_user(username=username, email=email, password=senha)
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
            return redirect('conta')  # Redireciona para a mesma página para ver as mudanças
    else:
        form = FotoPerfilForm(instance=request.user)

    # Passe tanto o formulário quanto o usuário para o contexto
    context = {'form': form, 'usuario': request.user}
    return render(request, 'conta.html', context)



