from rest_framework import serializers

from django.contrib.auth.models import User
from .models import Load, Kwh

class KwhSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kwh
        fields = ['user', 'load', 'kwh', 'timestamp',]