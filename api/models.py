from django.db import models
from django.contrib.auth.models import User

# Esses modelos descrevem tabelas no banco de dados.

# SuperUser:
# noseri_admin
# Password123

class Load(models.Model):
    """Esta tabela guarda informações a respeito das cargas."""
    load = models.CharField(max_length = 32)

    def __str__(self):
        return self.load
    

class Kwh(models.Model):
    """Este é o modelo (tabela) principal do Aplicativo."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    load = models.ForeignKey(Load, on_delete=models.CASCADE, default=None)
    kwh = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'User: {self.user} | Carga: {self.load} | Kwh: {self.kwh}'