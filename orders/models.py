from django.db import models
from accounts.models import CustomUser
# from django.dispatch import receiver
# from django.db.models.signals import post_save
# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer


class StoreBaker(models.Model):
    user = models.ForeignKey(CustomUser, models.CASCADE, related_name='user_store')
    store_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    logo = models.FileField(upload_to='logo/')
    store_status = models.CharField(max_length=100)

    objects = models.Manager()

    class Meta:
        verbose_name = "فروشگاه خرید نان"
        verbose_name_plural = "فروشگاه های خرید نان"

    def __str__(self):
        return f'{self.store_name}   {self.user}'


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_order')
    store = models.ForeignKey(StoreBaker, on_delete=models.CASCADE, related_name='store_order')
    order_code = models.IntegerField(unique=True)
    time = models.IntegerField()
    waiting_time = models.IntegerField()
    created_at = models.TimeField(auto_now_add=True)
    bread_number = models.IntegerField()
    # random_code = models.CharField(max_length=6, null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return f'order-code : {self.order_code} - bread-number : {self.bread_number} - waiting_time : {self.waiting_time} - time : {self.time}'

    class Meta:
        verbose_name = "نوبت ثبت شده"
        verbose_name_plural = "نوبت های ثبت شده"


class ReadyOrders(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_code = models.IntegerField()
    created_at = models.TimeField(auto_now_add=True)
    bread_number = models.IntegerField()

    objects = models.Manager()

    def __str__(self):
        return f'order code: {self.order_code} - bread_number: {self.bread_number}'

    class Meta:
        verbose_name = "نوبت در حال تحویل"
        verbose_name_plural = "نوبت های درحال تحویل"


# class QrCode_Generator(models.Model):
#     objects = models.Manager()
#
#
# channel_layer = get_channel_layer()
#
#
# @receiver(post_save, sender=Order)
# def send_order_change(sender, instance, created, **kwargs):
#     if created:
#         data = [{
#             'order_code': instance.order_code,
#             'waiting_time': instance.waiting_time,
#             'bread_number': instance.bread_number
#         }]
#         async_to_sync(channel_layer.group_send)('queue_group', {'type': 'send_change', 'data': data})
