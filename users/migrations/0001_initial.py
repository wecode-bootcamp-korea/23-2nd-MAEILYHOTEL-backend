# Generated by Django 3.2.6 on 2021-08-18 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stays', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=45)),
                ('email', models.CharField(max_length=2000)),
                ('password', models.CharField(max_length=200, null=True)),
                ('birth_date', models.DateField(null=True)),
                ('agreement', models.BooleanField(default=False)),
                ('point', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('kakao_id', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='UserLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('discount', models.FloatField()),
            ],
            options={
                'db_table': 'userlevels',
            },
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staytype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stays.staytype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
            options={
                'db_table': 'wishlists',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='userlevel',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.userlevel'),
        ),
    ]