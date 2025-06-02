from django.urls import path
from .views import TasksListView, UserTasksView, UserScoresView

urlpatterns = [
    path('tasks', TasksListView.as_view(), name='tasks-list'),
    path('user-tasks/<str:soeid>', UserTasksView.as_view(), name='user-tasks'),
    path('user-scores/', UserScoresView.as_view(), name='user-scores'),
]