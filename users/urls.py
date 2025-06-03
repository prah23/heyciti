from django.urls import path
from .views import CreateUserAndLinkTasksView, UpdateUserAvatarView, GetUserDetailsView, UpdateUserDetailsView

urlpatterns = [
    path('user/create', CreateUserAndLinkTasksView.as_view(), name='create-user'),
    path('user/<str:soeid>/avatar', UpdateUserAvatarView.as_view(), name='update-user-avatar'),
    path('user/<str:soeid>', GetUserDetailsView.as_view(), name='get-user-details'),
    path('user/<str:soeid>/update', UpdateUserDetailsView.as_view(), name='update-user-details'),
]