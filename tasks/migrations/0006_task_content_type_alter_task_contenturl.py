# Generated by Django 5.2.1 on 2025-06-03 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_module_task_module'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='content_type',
            field=models.CharField(choices=[('string', 'String'), ('ppt', 'PPT'), ('pdf', 'PDF'), ('url', 'URL'), ('mp4', 'MP4'), ('mp3', 'MP3')], default='url', max_length=10),
        ),
        migrations.AlterField(
            model_name='task',
            name='contentUrl',
            field=models.TextField(blank=True, null=True),
        ),
    ]
