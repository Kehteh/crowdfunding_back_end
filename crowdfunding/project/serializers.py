from rest_framework import serializers
from django.apps import apps

class PledgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model('project.Pledge')
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model('project.Project')
        fields = '__all__'

class ProjectDetailSerializer(ProjectSerializer):
    pledges = PledgeSerializer(many=True, read_only=True)