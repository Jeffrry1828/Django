# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-07 08:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('trade_no', models.CharField(max_length=200, verbose_name='支付流水号')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.OrderInfo', verbose_name='订单对象')),
            ],
            options={
                'db_table': 'tb_payments',
            },
        ),
    ]
