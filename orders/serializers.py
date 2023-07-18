from rest_framework import serializers
from orders.models import Order, StoreBaker


class InputSerializers(serializers.Serializer):
    store = serializers.CharField()
    order_code = serializers.CharField()
    bread_number = serializers.CharField()


class OutPut_Serializer_Create_Order_View(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='phone_number')
    store = serializers.SlugRelatedField(read_only=True, slug_field='store_name')

    class Meta:
        model = Order
        fields = ('user', 'store', 'order_code', 'bread_number', 'waiting_time')


class StoreSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='phone_number')

    class Meta:
        model = StoreBaker
        fields = '__all__'
