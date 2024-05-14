# Generated by Django 5.0.4 on 2024-05-07 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LittleLemonDRF', '0003_remove_order_total_alter_orderitem_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
    ]
