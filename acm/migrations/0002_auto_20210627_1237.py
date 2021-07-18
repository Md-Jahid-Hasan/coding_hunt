# Generated by Django 3.1.6 on 2021-06-27 06:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('acm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProblemSolving',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('url', models.URLField(max_length=255)),
                ('division', models.CharField(choices=[('B', 'Blue'), ('G', 'Green'), ('R', 'Red')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='UserSolveProblem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='acm.problemsolving')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='problemsolving',
            name='user',
            field=models.ManyToManyField(through='acm.UserSolveProblem', to=settings.AUTH_USER_MODEL),
        ),
    ]
