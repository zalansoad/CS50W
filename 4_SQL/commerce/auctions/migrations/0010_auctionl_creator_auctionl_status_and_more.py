# Generated by Django 5.2.1 on 2025-07-10 22:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_categories_alter_auctionl_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionl',
            name='creator',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='auctionl',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('closed', 'Closed'), ('pending', 'Pending')], default='active', max_length=10),
        ),
        migrations.AlterField(
            model_name='auctionl',
            name='bid_start',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
        migrations.AlterField(
            model_name='bids',
            name='bid',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
    ]
