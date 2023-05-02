# Generated by Django 4.1.7 on 2023-04-29 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_merge_20230423_2244'),
        ('post', '0005_remove_post_dislikes_remove_post_likes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_by', to='user.userinfo'),
        ),
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(blank=True, upload_to='image_post/'),
        ),
    ]