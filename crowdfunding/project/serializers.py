from rest_framework import serializers
from django.apps import apps

class PledgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model('project.Pledge')
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.anonymous:
            data.pop('supporter', None)
        return data



class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    
    class Meta:
        model = apps.get_model('project.Project')
        fields = '__all__'

class ProjectDetailSerializer(ProjectSerializer):
    pledges = PledgeSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
      instance.title = validated_data.get('title', instance.title)
      instance.description = validated_data.get('description', instance.description)
      instance.goal = validated_data.get('goal', instance.goal)
      instance.image = validated_data.get('image', instance.image)
      instance.is_open = validated_data.get('is_open', instance.is_open)
      instance.date_created = validated_data.get('date_created', instance.date_created)
      instance.owner = validated_data.get('owner', instance.owner)
      instance.save()
      return instance
    
