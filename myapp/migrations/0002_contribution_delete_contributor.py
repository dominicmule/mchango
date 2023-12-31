# Generated by Django 4.2.7 on 2023-11-29 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contribution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contributor_name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=20)),
                ('contribution_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('contributed_at', models.DateTimeField(auto_now_add=True)),
                ('mchango', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.mchango')),
            ],
        ),
        migrations.DeleteModel(
            name='Contributor',
        ),
    ]
