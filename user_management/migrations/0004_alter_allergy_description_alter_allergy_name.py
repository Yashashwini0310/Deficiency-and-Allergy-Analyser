# Generated by Django 4.2.19 on 2025-02-28 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0003_allergy_deficiency_userprofile_medical_history'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allergy',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='allergy',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
