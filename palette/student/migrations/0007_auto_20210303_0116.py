# Generated by Django 3.1.5 on 2021-03-02 17:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0006_answer_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='AssessmentID',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='student.assessment'),
        ),
    ]