from django.contrib import admin
from .models import Task, UserTask
from users.models import User

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'x', 'y', 'contentUrl')
    search_fields = ('name', 'contentUrl')

    def save_model(self, request, obj, form, change):
        """
        Override save_model to add the task to all users after creation.
        """
        super().save_model(request, obj, form, change)

        # If the task is newly created (not updated), link it to all users
        if not change:  # `change` is False for new objects
            users = User.objects.all()
            for user in users:
                UserTask.objects.get_or_create(user=user, task=obj)

@admin.register(UserTask)
class UserTaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'completed')  # Display user, task, and completed status
    search_fields = ('user__soeid', 'task__name')  # Allow searching by user SOEID and task name
    list_filter = ('completed',)  # Add a filter for the completed field