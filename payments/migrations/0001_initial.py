# Generated by Django 5.0.7 on 2024-07-15 23:33

import django.db.models.deletion
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=Decimal('0.00'), editable=False, max_digits=15)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('payee', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='payee_user', to=settings.AUTH_USER_MODEL)),
                ('payer', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
