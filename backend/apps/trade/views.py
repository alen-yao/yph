"""交易模块视图"""
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from .models import Cart, Order, OrderReturn, OrderReturnReason
from .serializers import (
    CartSerializer, OrderListSerializer, OrderDetailSerializer,
    OrderCreateSerializer, OrderReturnSerializer, OrderReturnReasonSerializer
)


class CartViewSet(viewsets.ModelViewSet):
    """
    购物车视图集
    对应 modulithshop 的 CartController
    """
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='add')
    def add_to_cart(self, request):
        """添加到购物车"""
        product_item_id = request.data.get('product_item_id')
        quantity = int(request.data.get('quantity', 1))

        # 检查是否已存在
        cart_item = Cart.objects.filter(
            user=request.user,
            product_item_id=product_item_id
        ).first()

        if cart_item:
            # 更新数量
            cart_item.quantity += quantity
            cart_item.save()
        else:
            # TODO: 从商品表获取商品信息
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            cart_item = serializer.instance

        return Response(CartSerializer(cart_item).data)

    @action(detail=False, methods=['post'], url_path='update-quantity')
    def update_quantity(self, request):
        """更新数量"""
        cart_id = request.data.get('cart_id')
        quantity = request.data.get('quantity')

        try:
            cart_item = Cart.objects.get(id=cart_id, user=request.user)
            cart_item.quantity = quantity
            cart_item.save()
            return Response({'message': '更新成功'})
        except Cart.DoesNotExist:
            return Response({'error': '购物车项不存在'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'], url_path='check')
    def check_items(self, request):
        """选中/取消选中"""
        cart_ids = request.data.get('cart_ids', [])
        is_checked = request.data.get('is_checked', True)

        Cart.objects.filter(id__in=cart_ids, user=request.user).update(is_checked=is_checked)
        return Response({'message': '操作成功'})

    @action(detail=False, methods=['post'], url_path='check-all')
    def check_all(self, request):
        """全选/取消全选"""
        is_checked = request.data.get('is_checked', True)
        Cart.objects.filter(user=request.user).update(is_checked=is_checked)
        return Response({'message': '操作成功'})

    @action(detail=False, methods=['delete'], url_path='clear')
    def clear_cart(self, request):
        """清空购物车"""
        Cart.objects.filter(user=request.user).delete()
        return Response({'message': '购物车已清空'})

    @action(detail=False, methods=['get'], url_path='count')
    def cart_count(self, request):
        """购物车数量"""
        count = Cart.objects.filter(user=request.user).count()
        return Response({'count': count})


class OrderViewSet(viewsets.ModelViewSet):
    """
    订单视图集
    对应 modulithshop 的 OrderController
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'pay_type']
    search_fields = ['order_sn', 'receiver_name', 'receiver_mobile']
    ordering_fields = ['created_time', 'total_amount']

    def get_queryset(self):
        # 管理员可以看所有订单，普通用户只能看自己的
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

    def get_permissions(self):
        # 列表、详情、创建允许认证用户，其他操作需要管理员
        if self.action in ['list', 'retrieve', 'create']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        elif self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderListSerializer

    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel_order(self, request, pk=None):
        """取消订单"""
        order = self.get_object()
        if order.status != 0:
            return Response({'error': '订单状态不允许取消'}, status=status.HTTP_400_BAD_REQUEST)

        order.status = 4
        order.cancel_time = timezone.now()
        order.save()
        return Response({'message': '订单已取消'})

    @action(detail=True, methods=['post'], url_path='confirm-receipt')
    def confirm_receipt(self, request, pk=None):
        """确认收货"""
        order = self.get_object()
        if order.status != 2:
            return Response({'error': '订单状态错误'}, status=status.HTTP_400_BAD_REQUEST)

        order.status = 3
        order.finish_time = timezone.now()
        order.save()
        return Response({'message': '确认收货成功'})

    @action(detail=True, methods=['post'], url_path='pay')
    def pay_order(self, request, pk=None):
        """支付订单"""
        order = self.get_object()
        if order.status != 0:
            return Response({'error': '订单状态错误'}, status=status.HTTP_400_BAD_REQUEST)

        pay_type = request.data.get('pay_type')
        # TODO: 调用支付接口
        # 这里暂时直接标记为已支付
        order.status = 1
        order.pay_type = pay_type
        order.pay_time = timezone.now()
        order.save()

        return Response({
            'message': '支付成功',
            'order_no': order.order_no
        })

    @action(detail=False, methods=['get'], url_path='status-count')
    def status_count(self, request):
        """各状态订单数量"""
        user = request.user
        return Response({
            'unpaid': Order.objects.filter(user=user, status=0).count(),
            'unshipped': Order.objects.filter(user=user, status=1).count(),
            'unreceived': Order.objects.filter(user=user, status=2).count(),
            'completed': Order.objects.filter(user=user, status=3).count(),
        })


class OrderReturnViewSet(viewsets.ModelViewSet):
    """
    退货退款视图集
    对应 modulithshop 的 ReturnController
    """
    serializer_class = OrderReturnSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return OrderReturn.objects.filter(user=self.request.user)


class OrderReturnReasonViewSet(viewsets.ReadOnlyModelViewSet):
    """退货原因视图集"""
    queryset = OrderReturnReason.objects.filter(is_enable=True)
    serializer_class = OrderReturnReasonSerializer
    permission_classes = [permissions.AllowAny]
