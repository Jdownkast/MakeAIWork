# Generated by Django 4.1.5 on 2023-01-29 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Netlify',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genetic', models.IntegerField(null=True)),
                ('length', models.IntegerField(null=True)),
                ('mass', models.IntegerField(null=True)),
                ('exercise', models.IntegerField(null=True)),
                ('smoking', models.IntegerField(null=True)),
                ('alcohol', models.IntegerField(null=True)),
                ('sugar', models.IntegerField(null=True)),
                ('lifespan', models.IntegerField(null=True)),
            ],
        ),
    ]
