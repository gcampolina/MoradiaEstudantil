from django.contrib import admin
from django.urls import path
from AppMoradia import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('sistema/', views.dashboard, name='sistema'),
    path('conta/', views.conta, name='conta'),
    path('eventos/', views.eventos, name='eventos'),
    path('avisos/', views.avisos, name='avisos'),
    path('adicionar_evento/', views.adicionar_evento, name='adicionar_evento'),
    path('excluir_evento/<int:evento_id>/', views.excluir_evento, name='excluir_evento'),
    path('adicionar_aviso/', views.adicionar_aviso, name='adicionar_aviso'),
    path('excluir_aviso/<int:aviso_id>/', views.excluir_aviso, name='excluir_aviso'),
    path('enquetes/', views.enquetes, name='enquetes'),
    path('criar_enquete/', views.criar_enquete, name='criar_enquete'),
    path('excluir_enquete/<int:enquete_id>/', views.excluir_enquete, name='excluir_enquete'),
    path('enquetes/<int:enquete_id>/votar/', views.votar_enquete, name='votar_enquete'),
    path('resultado/enquete/<int:enquete_id>/', views.resultados_enquete, name='enquete_resultado'),
    path('detalhes-enquete/<int:enquete_id>/', views.detalhes_enquete, name='detalhes_enquete'),
    path('enquetes/<int:enquete_id>/encerrar/', views.encerrar_enquete, name='encerrar_enquete'),
    path('painel-controle/', views.painelcontrole, name='painel-controle'),
    path('painel-controle/update_user/<int:user_id>/', views.update_user, name='update_user'),
    path('painel-controle/delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
