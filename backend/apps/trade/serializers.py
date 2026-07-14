"""交易模块序列化器"""
from rest_framework import serializers
from .models import Cart, Order, OrderItem, OrderLogistics, OrderReturn, OrderReturnReason
from decimal import Decimal
import time


class CartSerializer(serializers.ModelSerializer):
    """购物车序列化器"""
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'product_id', 'product_item_id', 'product_name', 'product_image',
                  'price', 'quantity', 'is_checked', 'subtotal', 'created_time']
        read_only_fields = ['id', 'created_time']

    def get_subtotal(self, obj):
        return obj.subtotal()

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class OrderItemSerializer(serializers.ModelSerializer):
    """订单商品序列化器"""
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderLogisticsSerializer(serializers.ModelSerializer):
    """订单物流序列化器"""
    class Meta:
        model = OrderLogistics
        fields = '__all__'


class OrderListSerializer(serializers.ModelSerializer):
    """订单列表序列化器"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    item_count = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'order_no', 'order_amount', 'freight_amount', 'discount_amount',
                  'pay_amount', 'status', 'status_display', 'item_count', 'created_time']

    def get_item_count(self, obj):
        return obj.items.count()


class OrderDetailSerializer(serializers.ModelSerializer):
    """订单详情序列化器"""
    items = OrderItemSerializer(many=True, read_only=True)
    logistics = OrderLogisticsSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class OrderCreateSerializer(serializers.Serializer):
    """创建订单序列化器"""
    address_id = serializers.IntegerField(help_text='收货地址ID')
    cart_ids = serializers.ListField(
        child=serializers.IntegerField(),
        help_text='购物车ID列表'
    )
    user_remark = serializers.CharField(required=False, allow_blank=True, help_text='买家备注')
    pay_type = serializers.IntegerField(required=False, help_text='支付方式')

    def validate_address_id(self, value):
        from users.models import DeliveryAddress
        user = self.context['request'].user
        if not DeliveryAddress.objects.filter(id=value, user=user).exists():
            raise serializers.ValidationError('收货地址不存在')
        return value

    def validate_cart_ids(self, value):
        if not value:
            raise serializers.ValidationError('请选择商品')
        user = self.context['request'].user
        carts = Cart.objects.filter(id__in=value, user=user)
        if carts.count() != len(value):
            raise serializers.ValidationError('购物车商品不存在')
        return value

    def create(self, validated_data):
        from users.models import DeliveryAddress
        user = self.context['request'].user

        # 获取收货地址
        address = DeliveryAddress.objects.get(id=validated_data['address_id'], user=user)

        # 获取购物车商品
        carts = Cart.objects.filter(id__in=validated_data['cart_ids'], user=user)

        # 计算金额
        order_amount = sum([cart.subtotal() for cart in carts])
        freight_amount = Decimal('0.00')  # 运费计算逻辑
        discount_amount = Decimal('0.00')  # 优惠金额计算逻辑
        pay_amount = order_amount + freight_amount - discount_amount

        # 生成订单号
        order_no = f'ORD{int(time.time() * 1000)}{user.id}'

        # 创建订单
        order = Order.objects.create(
            order_no=order_no,
            user=user,
            order_amount=order_amount,
            freight_amount=freight_amount,
            discount_amount=discount_amount,
            pay_amount=pay_amount,
            consignee=address.consignee,
            mobile=address.mobile,
            province=address.province,
            city=address.city,
            district=address.district,
            address=address.address,
            user_remark=validated_data.get('user_remark', ''),
            pay_type=validated_data.get('pay_type')
        )

        # 创建订单商品
        order_items = []
        for cart in carts:
            order_items.append(OrderItem(
                order=order,
                product_id=cart.product_id,
                product_name=cart.product_name,
                product_image=cart.product_image,
                product_item_id=cart.product_item_id,
                sku_name='',  # 从商品获取
                price=cart.price,
                quantity=cart.quantity,
                total_amount=cart.subtotal()
            ))
        OrderItem.objects.bulk_create(order_items)

        # 清空购物车
        carts.delete()

        return order


class OrderReturnReasonSerializer(serializers.ModelSerializer):
    """退货原因序列化器"""
    class Meta:
        model = OrderReturnReason
        fields = '__all__'


class OrderReturnSerializer(serializers.ModelSerializer):
    """退货退款序列化器"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = OrderReturn
        fields = '__all__'
        read_only_fields = ['return_no', 'user', 'status', 'admin_remark']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        # 生成退款单号
        validated_data['return_no'] = f'RET{int(time.time() * 1000)}{user.id}'
        return super().create(validated_data)
