from django.shortcuts import render
from rest_framework.views import APIView
from orders import serializers
from orders.models import Order, StoreBaker
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import random
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema


# from orders.models import QrCode_Generator


class CreateOrderApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    @extend_schema(request=serializers.InputSerializers, responses=serializers.OutPut_Serializer_Create_Order_View)
    def post(self, request):
        user = request.user
        if user.is_baker:
            ser_data = serializers.InputSerializers(data=request.POST)
        else:
            data = request.data.copy()
            store = StoreBaker.objects.get(store_name=data['store'])
            if user.user_order.filter(store=store).exists():
                order = user.user_order.get(store=store)
                print(order)
                ser_data = serializers.OutPut_Serializer_Create_Order_View(instance=order)
                return Response(ser_data.data, status.HTTP_200_OK)

            else:
                id_obj = QrCode_Generator.objects.create()
                data['order_code'] = id_obj.pk
                ser_data = serializers.InputSerializers(data=data)

        if ser_data.is_valid():
            order_code = ser_data.validated_data['order_code']
            if Order.objects.filter(order_code=order_code).exists():
                ord_obj = Order.objects.get(order_code=order_code)

                ins_data_user = serializers.OutPut_Serializer_Create_Order_View(instance=ord_obj)
                if request.user.is_baker:
                    store = ord_obj.store
                    ins_data_store = serializers.StoreSerializer(instance=store)
                    data = {'user_baker': ins_data_user.data, 'store': ins_data_store.data}
                    return Response(data, status.HTTP_200_OK)
                else:
                    return Response(ins_data_user.data, status.HTTP_200_OK)
            bread_number = int(ser_data.validated_data['bread_number'])
            store_name = ser_data.validated_data['store']
            store_obj = get_object_or_404(StoreBaker, store_name=store_name)
            time_sec = bread_number * 20
            last_order = Order.objects.order_by('-created_at').first()

            if last_order is not None:
                waiting_time = last_order.waiting_time + time_sec
            else:
                waiting_time = time_sec

            order_numbers = Order.objects.create(user=request.user,
                                                 store=store_obj,
                                                 order_code=order_code,
                                                 time=time_sec,
                                                 waiting_time=waiting_time,
                                                 bread_number=bread_number)
            ins_data = serializers.OutPut_Serializer_Create_Order_View(instance=order_numbers)
            return Response(ins_data.data, status.HTTP_200_OK)
        return Response(ser_data.errors, status.HTTP_400_BAD_REQUEST)

# class SendAllStore(APIView):
#     serializer_class = serializers.StoreSerializer
#     permission_classes = [IsAuthenticated, ]
#
#     def post(self, request):
#         all_store = StoreBaker.objects.all()
#         ins_data = serializers.StoreSerializer(instance=all_store, many=True)
#         return Response(ins_data.data, status.HTTP_200_OK)
