# Generated by Django 4.1.6 on 2023-04-23 15:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_userinfo_last_logout_userinfo_online_status'),
        ('openChat', '0003_alter_message_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openchat',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='open_chat_created_by', to='user.userinfo'),
        ),
    ]