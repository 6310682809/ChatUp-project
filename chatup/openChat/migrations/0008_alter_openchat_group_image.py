# Generated by Django 4.1.6 on 2023-04-24 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openChat', '0007_alter_openchat_group_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openchat',
            name='group_image',
            field=models.ImageField(blank=True, default='./static/openChat/img/avatar.jpg', upload_to='uploads/'),
        ),
    ]
