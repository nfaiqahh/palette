# Generated by Django 3.1.5 on 2021-01-21 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_delete_request'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessment',
            name='AssignedClass',
            field=models.ManyToManyField(to='student.Class'),
        ),
        migrations.AddField(
            model_name='student',
            name='RegisteredClass',
            field=models.ManyToManyField(to='student.Class'),
        ),
    ]