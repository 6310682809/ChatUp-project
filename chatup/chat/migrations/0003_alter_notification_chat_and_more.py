# Generated by Django 4.1.6 on 2023-04-18 22:49

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_post_dislikes_post_likes_delete_like'),
        ('chat', '0002_alter_chat_reciever_alter_chat_sender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='chat',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='noti_chat', to='chat.chat'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='created_at',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='noti_post', to='post.post'),
        ),
    ]
