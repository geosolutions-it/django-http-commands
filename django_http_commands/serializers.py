from rest_framework import serializers
from .models import ManagementCommand


class ManagementCommandSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ManagementCommand
        fields = ['name', 'app']
