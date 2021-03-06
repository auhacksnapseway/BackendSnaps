# Generated by Django 2.2 on 2019-04-05 20:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backendsnaps', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_datetime', models.DateTimeField(auto_now_add=True)),
                ('end_datetime', models.DateTimeField(blank=True, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_events', to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(related_name='events', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DrinkEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='drink_events', to='backendsnaps.Event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='drink_events', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
