# Generated by Django 3.1.5 on 2021-01-20 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='Topics',
            field=models.ManyToManyField(to='student.CourseTopic'),
        ),
    ]