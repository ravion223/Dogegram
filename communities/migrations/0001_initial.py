# Generated by Django 5.0.6 on 2024-07-23 14:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('community_logo', models.ImageField(blank=True, null=True, upload_to='communities/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('members', models.ManyToManyField(related_name='community_members', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='communities', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Community',
                'verbose_name_plural': 'Communities',
                'ordering': ['created_at'],
            },
        ),
    ]
