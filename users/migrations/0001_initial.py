# Generated by Django 4.1.5 on 2023-01-31 00:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('capacity', models.IntegerField(default=0)),
                ('creation_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('description', models.TextField(default='')),
                ('date', models.DateTimeField()),
                ('creation_date', models.DateTimeField(auto_now=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.room')),
            ],
        ),
        migrations.CreateModel(
            name='Attendant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscription_date', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]