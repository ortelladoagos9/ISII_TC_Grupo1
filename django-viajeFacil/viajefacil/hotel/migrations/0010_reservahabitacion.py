# Generated by Django 5.2 on 2025-04-28 02:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0009_habitacion'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReservaHabitacion',
            fields=[
                ('id_reserva', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_reserva', models.DateField()),
                ('estado_reserva', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.estadoreserva')),
                ('habitacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.habitacion')),
            ],
            options={
                'verbose_name': 'Reserva de Habitación',
                'verbose_name_plural': 'Reservas de Habitaciones',
                'unique_together': {('id_reserva', 'habitacion')},
            },
        ),
    ]
