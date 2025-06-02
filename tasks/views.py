from django.db.models import Sum, F, Min, IntegerField
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Task, UserTask
from users.models import User
from .serializers import TaskSerializer, TaskViewSerializer, UserTaskSerializer


class TasksListView(APIView):
    """
    View to list all tasks in the database.
    """

    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskViewSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserTasksView(APIView):
    """
    View to list and update tasks for a specific user.
    """

    def get(self, request, soeid):
        # Get the user by SOEID
        try:
            user = User.objects.get(soeid=soeid)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Get all tasks for the user
        user_tasks = UserTask.objects.filter(user=user)
        serializer = UserTaskSerializer(user_tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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