# Generated by Django 3.1.5 on 2021-01-22 05:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_auto_20210121_2120'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessment',
            name='Lecturer',
            field=models.ForeignKey(default='11', on_delete=django.db.models.deletion.CASCADE, to='student.lecturer'),
        ),
    ]
