# Generated by Django 5.0.1 on 2024-02-16 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('handleBlog', '0007_alter_blog_blogimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='blogImage',
            field=models.ImageField(upload_to='image'),
        ),
    ]