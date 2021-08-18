# Generated by Django 3.2.6 on 2021-08-18 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'facilities',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('quantity', models.IntegerField()),
                ('image_url', models.CharField(max_length=2000)),
                ('people', models.PositiveIntegerField()),
            ],
            options={
                'db_table': 'rooms',
            },
        ),
        migrations.CreateModel(
            name='Staytype',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('address', models.CharField(max_length=2000)),
                ('longitude', models.DecimalField(decimal_places=7, max_digits=10)),
                ('latitude', models.DecimalField(decimal_places=7, max_digits=10)),
                ('description', models.TextField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='stays.category')),
            ],
            options={
                'db_table': 'staytypes',
            },
        ),
        migrations.CreateModel(
            name='StaytypeImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.CharField(max_length=2000)),
                ('staytype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stays.staytype')),
            ],
            options={
                'db_table': 'staytypeimages',
            },
        ),
        migrations.CreateModel(
            name='StaytypeFacility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stays.facility')),
                ('staytype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stays.staytype')),
            ],
            options={
                'db_table': 'staytypes_facilities',
            },
        ),
        migrations.AddField(
            model_name='staytype',
            name='facility',
            field=models.ManyToManyField(related_name='staytypes', through='stays.StaytypeFacility', to='stays.Facility'),
        ),
        migrations.CreateModel(
            name='RoomOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('check_in', models.TimeField()),
                ('check_out', models.TimeField()),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='stays.room')),
            ],
            options={
                'db_table': 'roomoptions',
            },
        ),
        migrations.AddField(
            model_name='room',
            name='staytype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='stays.staytype'),
        ),
    ]