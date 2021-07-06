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


class BillingInfo(models.Model):
    """
    Tabela responsável por armazenar os dados da fatura do cliente. 
    """

    grupo_choices = [
        ("A", "Grupo A"),
        ("B", "Grupo B"),
    ]

    sub_grupo_choices = [
        ("A1", "A1"),
        ("A2", "A2"),
        ("A3", "A3"),
        ("A3a", "A3a"),
        ("A4", "A4"),
        ("AS", "AS"),
        ("B1", "B1"),
        ("B2", "B2"),
        ("B3", "B3"),
        ("B4", "B4"),
    ]

    modalidade_choices = [
        ("Convencional", "Convencional"),
        ("Azul", "Azul"),
        ("Branca", "Branca"),
        ("Verde", "Verde"),
    ]

    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE, default=None)
    grupo = models.CharField(max_length=1, choices=grupo_choices)
    sub_grupo = models.CharField(max_length=3, choices=sub_grupo_choices)
    modalidade_tarifaria = models.CharField(max_length=12, choices=modalidade_choices)

    def __str__(self):
        return f"Cliente: {self.user}"


class Student(models.Model):
    FRESHMAN = 'FR'
    SOPHOMORE = 'SO'
    JUNIOR = 'JR'
    SENIOR = 'SR'
    GRADUATE = 'GR'
    YEAR_IN_SCHOOL_CHOICES = [
        (FRESHMAN, 'Freshman'),
        (SOPHOMORE, 'Sophomore'),
        (JUNIOR, 'Junior'),
        (SENIOR, 'Senior'),
        (GRADUATE, 'Graduate'),
    ]
    year_in_school = models.CharField(
        max_length=2,
        choices=YEAR_IN_SCHOOL_CHOICES,
        default=FRESHMAN,
    )

    def is_upperclass(self):
        return self.year_in_school in {self.JUNIOR, self.SENIOR}