from celery import shared_task
from orders.models import Order, ReadyOrders
from datetime import datetime, timedelta
import pytz


@shared_task
def update_waiting_time():
    orders = Order.objects.all()
    ready_orders = []

    for order in orders:
        if order.waiting_time <= 0:
            ready_orders.append(order)
        else:
            order.waiting_time = str(int(order.waiting_time) - 1)
            order.save()
    if ready_orders:
        ReadyOrders.objects.bulk_create(
            [ReadyOrders(user=order.user, order_code=order.order_code, bread_number=order.bread_number) for order in ready_orders])
        Order.objects.filter(id__in=[order.id for order in ready_orders]).delete()



@shared_task()
def delete_ready_order():
    expired_time = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(seconds=20)
    ReadyOrders.objects.filter(created_at__lt=expired_time).delete()
