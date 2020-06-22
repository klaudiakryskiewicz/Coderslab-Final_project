# Generated by Django 3.0.7 on 2020-06-22 14:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(choices=[('F', 'Kobieta'), ('M', 'Mężczyzna'), ('None', '-')], default='None', max_length=9)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gift_wishes.Family')),
            ],
        ),
        migrations.CreateModel(
            name='Wish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('description', models.TextField()),
                ('link', models.CharField(max_length=300)),
                ('price', models.IntegerField()),
                ('Member', models.ManyToManyField(to='gift_wishes.Member')),
            ],
        ),
        migrations.CreateModel(
            name='Present',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_bought', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('wish', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='gift_wishes.Wish')),
            ],
        ),
    ]
