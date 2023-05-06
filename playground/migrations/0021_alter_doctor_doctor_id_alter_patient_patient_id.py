# Generated by Django 4.1 on 2023-04-27 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0020_alter_doctor_doctor_id_alter_patient_patient_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='doctor_id',
            field=models.IntegerField(default=69414, editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='patient_id',
            field=models.IntegerField(default=13307, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
