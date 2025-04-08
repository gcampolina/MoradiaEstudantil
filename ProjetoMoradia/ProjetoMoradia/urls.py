from django.contrib import admin
from django.urls import path
from AppMoradia import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
