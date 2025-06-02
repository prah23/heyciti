from rest_framework import serializers
from .models import Task, UserTask
from users.models import User

class TaskViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        exclude = ('id',)


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('name', 'completed')


class UserTaskSerializer(serializers.ModelSerializer):
    task_name = serializers.CharField(source='task.name', read_only=True)
    user_soeid = serializers.CharField(source='user.soeid', read_only=True)

    class Meta:
        model = UserTask
        fields = ('user_soeid', 'task_name', 'completed')