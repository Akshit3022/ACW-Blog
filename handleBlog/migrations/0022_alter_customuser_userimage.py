# Generated by Django 5.0.2 on 2024-03-05 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('handleBlog', '0021_customuser_userimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='userImage',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
