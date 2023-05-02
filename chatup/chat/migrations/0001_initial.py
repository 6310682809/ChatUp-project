# Generated by Django 4.1.2 on 2023-02-15 16:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('post', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('file', models.FileField(blank=True, upload_to='uploads/')),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('reciever', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_to', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_from', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_read', models.BooleanField(default=False)),
                ('detail', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('chat', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='noti_chat', to='chat.chat')),
                ('post', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='noti_post', to='post.post')),
                ('reciever', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='noti_reciever', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]