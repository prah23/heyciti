from django.urls import path
from .views import CreateUserAndLinkTasksView

urlpatterns = [
    path('user/create', CreateUserAndLinkTasksView.as_view(), name='create-user'),
]