# Generated by Django 5.0.1 on 2024-02-22 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('handleBlog', '0017_customuser_forgetpasstoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='userPhone',
            field=models.CharField(max_length=10),
        ),
    ]