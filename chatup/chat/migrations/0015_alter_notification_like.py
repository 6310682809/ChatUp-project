# Generated by Django 4.1.7 on 2023-04-29 18:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_alter_comment_created_by_alter_file_file'),
        ('chat', '0014_alter_notification_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='like',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='like', to='post.like'),
        ),
    ]
