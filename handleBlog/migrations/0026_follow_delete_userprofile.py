# Generated by Django 5.0.2 on 2024-03-07 09:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('handleBlog', '0025_alter_userprofile_followers_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_followers', to='handleBlog.customuser')),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_follows', to='handleBlog.customuser')),
            ],
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
