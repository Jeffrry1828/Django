from django.db import models
from utils.models import BaseModel


class Payment(BaseModel):
    order = models.ForeignKey('orders.OrderInfo', verbose_name='订单对象')
    trade_no = models.CharField(max_length=200, verbose_name='支付流水号')

    class Meta:
        db_table = 'tb_payments'
