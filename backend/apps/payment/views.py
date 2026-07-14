"""支付模块视图"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import PaymentOrder
import time


class PaymentViewSet(viewsets.GenericViewSet):
    """支付视图集"""
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='create')
    def create_payment(self, request):
        """创建支付订单"""
        order_id = request.data.get('order_id')
        pay_type = request.data.get('pay_type')
        pay_amount = request.data.get('pay_amount')

        # 生成支付单号
        payment_no = f'PAY{int(time.time() * 1000)}{request.user.id}'

        payment = PaymentOrder.objects.create(
            payment_no=payment_no,
            order_id=order_id,
            user=request.user,
            pay_type=pay_type,
            pay_amount=pay_amount
        )

        # TODO: 调用实际的支付接口
        if pay_type == 1:
            # 微信支付
            return Response({'message': '微信支付接口待实现', 'payment_no': payment_no})
        elif pay_type == 2:
            # 支付宝
            return Response({'message': '支付宝接口待实现', 'payment_no': payment_no})
        elif pay_type == 3:
            # 余额支付
            return Response({'message': '余额支付接口待实现', 'payment_no': payment_no})

    @action(detail=False, methods=['post'], url_path='notify')
    def payment_notify(self, request):
        """支付回调"""
        # TODO: 处理支付回调
        return Response({'message': 'success'})
