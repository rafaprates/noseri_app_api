from rest_framework import serializers

from django.contrib.auth.models import User
from .models import Load, Kwh, TrackedLoads

class KwhSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    load = serializers.ReadOnlyField(source='load.load')

    class Meta:
        model = Kwh
        fields = ['user', 'load', 'kwh', 'timestamp',]


class LoadSerializer(serializers.ModelSerializer):
    load = serializers.CharField()
        
    class Meta:
        model = Load
        fields = ["load"]


class TrackedLoadsSerializer(serializers.ModelSerializer):
    load = serializers.CharField()
    isTracked = serializers.BooleanField()

    class Meta:
        model = TrackedLoads
        fields = ["load", "isTracked"]

class ReaisSerializer(serializers.Serializer):
    load = serializers.CharField()
    kwh = serializers.FloatField()


class TotalKwhSerializer(serializers.Serializer):
    kwh_sum = serializers.FloatField()
    data = serializers.CharField()


class TotalByLoadSerializer(serializers.Serializer):
    load_name = serializers.CharField()
    kwh_sum = serializers.FloatField()

