# Generated by Django 2.1.5 on 2019-02-09 12:32

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('db_layer', '0004_user_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified_on', models.DateTimeField(auto_now=True, db_index=True)),
                ('place_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('display_name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('display_address', models.TextField(blank=True)),
                ('lat', models.DecimalField(decimal_places=6, max_digits=9)),
                ('lng', models.DecimalField(decimal_places=6, max_digits=9)),
                ('is_booked', models.BooleanField(default=False)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('google_place_id', models.CharField(blank=True, max_length=255)),
                ('is_deleted', models.BooleanField(default=False)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='db_layer.Location')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
