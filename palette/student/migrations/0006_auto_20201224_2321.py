# Generated by Django 3.1.1 on 2020-12-24 15:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('student', '0005_admin_userid'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessment',
            name='CourseID',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='student.course'),
        ),
        migrations.AddField(
            model_name='class',
            name='CourseID',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='student.course'),
        ),
        migrations.AddField(
            model_name='class',
            name='Lecturer',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='student.lecturer'),
        ),
        migrations.AddField(
            model_name='course',
            name='Course_Description',
            field=models.TextField(default='Description'),
        ),
        migrations.AddField(
            model_name='courseobjective',
            name='CourseID',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='student.course'),
        ),
        migrations.AddField(
            model_name='coursetopic',
            name='CourseID',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='student.course'),
        ),
        migrations.AddField(
            model_name='question',
            name='AssessmentID',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.PROTECT, to='student.assessment'),
        ),
        migrations.AddField(
            model_name='request',
            name='CourseID',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='student.course'),
        ),
        migrations.AddField(
            model_name='request',
            name='Requestor',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='student.lecturer'),
        ),
        migrations.AlterField(
            model_name='admin',
            name='UserID',
            field=models.OneToOneField(default='ID Number', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, to_field='username'),
        ),
        migrations.AlterField(
            model_name='assessment',
            name='AssessmentID',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='CourseID',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='lecturer',
            name='UserID',
            field=models.OneToOneField(default='ID Number', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, to_field='username'),
        ),
    ]
