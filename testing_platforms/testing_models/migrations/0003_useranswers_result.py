# Generated by Django 4.2.20 on 2025-07-22 21:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testing_models', '0002_alter_useranswers_answer_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='useranswers',
            name='result',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='testing_models.result'),
        ),
    ]
