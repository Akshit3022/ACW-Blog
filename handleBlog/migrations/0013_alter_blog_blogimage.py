# Generated by Django 5.0.1 on 2024-02-16 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('handleBlog', '0012_alter_blog_blogimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='blogImage',
            field=models.ImageField(upload_to='media'),
        ),
    ]
