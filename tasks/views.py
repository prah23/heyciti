from django.db.models import Sum, F, Min, IntegerField
from django.shortcuts import render
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Task, UserTask, Module
from users.models import User
from .serializers import TaskSerializer, TaskViewSerializer, UserTaskSerializer


class TasksListView(APIView):
    """
    View to list all modules with their tasks in the specified structure.
    """

    def get(self, request):
        modules = Module.objects.prefetch_related('tasks')

        response_data = []
        for module in modules:
            task_zone = [
                {
                    'name': task.name,
                    'x': task.x,
                    'y': task.y,
                    'contentUrl': task.contentUrl,
                    'content_type': task.content_type,
                }
                for task in module.tasks.all()
            ]
            response_data.append({
                'module_name': module.name,
                'map': module.map if module.map else None,
                'taskZone': task_zone,
            })

        return Response(response_data, status=status.HTTP_200_OK)


class UserTasksView(APIView):
    """
    View to list and update tasks for a specific user in the same structure as TasksListView.
    """

    def get(self, request, soeid):
        # Get the user by SOEID
        try:
            user = User.objects.get(soeid=soeid)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Get all UserTask objects for the user
        user_tasks = UserTask.objects.filter(user=user).select_related('task__module')

        # Group tasks by module
        modules = {}
        for user_task in user_tasks:
            module = user_task.task.module
            if module not in modules:
                modules[module] = {
                    'module_name': module.name,
                    'map': module.map if module.map else None,
                    'taskZone': []
                }
            modules[module]['taskZone'].append({
                'name': user_task.task.name,
                'x': user_task.task.x,
                'y': user_task.task.y,
                'completed': user_task.completed,
                'contentUrl': user_task.task.contentUrl,
                'content_type': user_task.task.content_type,
            })

        # Convert the grouped modules into a list
        response_data = list(modules.values())

        return Response(response_data, status=status.HTTP_200_OK)

    def patch(self, request, soeid):
        # Get the user by SOEID
        try:
            user = User.objects.get(soeid=soeid)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Update the 'completed' state for a specific task
        task_name = request.data.get('task_name')
        completed = request.data.get('completed')

        if task_name is None or completed is None:
            return Response({'error': 'Both task_name and completed are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_task = UserTask.objects.get(user=user, task__name=task_name)
            user_task.completed = completed
            if completed:  # Set completion_time only if completed is True
                user_task.completion_time = now()
            else:
                user_task.completion_time = None  # Reset if completed is set to False
            user_task.save()
        except UserTask.DoesNotExist:
            return Response({'error': 'Task not found for this user.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'message': 'Task updated successfully.'}, status=status.HTTP_200_OK)


class UserScoresView(APIView):
    """
    Endpoint to return a list of all users sorted by their score.
    If multiple users have the same score, rank them by the earliest completion time.
    """

    def get(self, request):
        users = User.objects.annotate(
            score=Sum(F('user_tasks__completed') * 10, output_field=IntegerField()),
            earliest_completion=Min('user_tasks__completion_time')
        ).order_by('-score', 'earliest_completion')

        user_scores = [
            {
                'soeid': user.soeid,
                'score': user.score or 0,
            }
            for user in users
        ]

        return Response(user_scores, status=status.HTTP_200_OK)