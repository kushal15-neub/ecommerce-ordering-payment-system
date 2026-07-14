from rest_framework import serializers

from .models import Order, OrderItem


# -----------------------------------------
# Order Item Serializer
# -----------------------------------------
class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem

        fields = [
            'id',
            'product',
            'quantity',
            'price',
            'subtotal'
        ]

        read_only_fields = [
            'price',
            'subtotal'
        ]


# -----------------------------------------
# Order Serializer
# -----------------------------------------
class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order

        fields = [
            'id',
            'user',
            'total_amount',
            'status',
            'created_at',
            'updated_at',
            'items'
        ]

        read_only_fields = [
            'total_amount',
            'status',
            'created_at',
            'updated_at'
        ]

    def create(self, validated_data):

        items_data = validated_data.pop('items')

        order = Order.objects.create(
            **validated_data
        )

        total_amount = 0

        for item_data in items_data:

            product = item_data['product']
            quantity = item_data['quantity']

            price = product.price
            subtotal = quantity * price

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price,
                subtotal=subtotal
            )

            total_amount += subtotal

        order.total_amount = total_amount
        order.save()

        return order

    def update(self, instance, validated_data):

        validated_data.pop('items', None)

        return super().update(
            instance,
            validated_data
        )