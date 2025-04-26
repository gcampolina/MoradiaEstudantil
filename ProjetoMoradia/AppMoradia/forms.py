from django import forms
from .models import CustomUser

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'foto', 'tipo')

class FotoPerfilForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['foto']