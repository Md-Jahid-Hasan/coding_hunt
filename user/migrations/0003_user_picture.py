# Generated by Django 3.1.6 on 2021-06-21 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='picture',
            field=models.URLField(default='www.google.com', max_length=255),
            preserve_default=False,
        ),
    ]
