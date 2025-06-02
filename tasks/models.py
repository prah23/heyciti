from django.db import models
from users.models import User

class Task(models.Model):
    name = models.CharField(max_length=255, unique=True)
    x = models.FloatField()
    y = models.FloatField()
    contentUrl = models.URLField(max_length=2048)

    def __str__(self):
        return self.name


class UserTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_tasks')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='user_tasks')
    completed = models.BooleanField(default=False)
    completion_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'task')  # Ensure a user-task pair is unique

    def __str__(self):
        return f"{self.user.soeid} - {self.task.name}"