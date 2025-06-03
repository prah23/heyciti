from django.db import models
from users.models import User


class Module(models.Model):
    name = models.CharField(max_length=255, unique=True)
    map = models.CharField(max_length=2048, null=True, blank=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('string', 'String'),
        ('ppt', 'PPT'),
        ('pdf', 'PDF'),
        ('url', 'URL'),
        ('mp4', 'MP4'),
        ('mp3', 'MP3'),
    ]

    name = models.CharField(max_length=255, unique=True)
    x = models.FloatField()
    y = models.FloatField()
    contentUrl = models.TextField(null=True, blank=True)  # Store text instead of URLs
    content_type = models.CharField(
        max_length=10,
        choices=CONTENT_TYPE_CHOICES,
        default='url'  # Default value is 'url'
    )
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)

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