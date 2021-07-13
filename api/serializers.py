from rest_framework import serializers

from django.contrib.auth.models import User
from .models import Load, Kwh

class KwhSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source='user.username')
    load = serializers.ReadOnlyField(source='load.load')


    class Meta:
        model = Kwh
        fields = ['user', 'load', 'kwh', 'timestamp',]