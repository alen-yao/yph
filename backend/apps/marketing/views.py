"""营销模块视图"""
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from datetime import timedelta
from .models import ActivityBase, Coupon, UserCoupon
from .serializers import (ActivitySerializer, ActivityCreateUpdateSerializer,
                          CouponSerializer, CouponCreateUpdateSerializer,
                          UserCouponSerializer)


class ActivityViewSet(viewsets.ModelViewSet):
    """营销活动视图集"""
    queryset = ActivityBase.objects.all()
    serializer_class = ActivitySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['activity_type', 'activity_state', 'is_enable']
    search_fields = ['activity_name', 'activity_desc']
    ordering_fields = ['start_time', 'end_time', 'created_time']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        queryset = ActivityBase.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_enable=True)
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ActivityCreateUpdateSerializer
        return ActivitySerializer


class CouponViewSet(viewsets.ModelViewSet):
    """优惠券视图集"""
    serializer_class = CouponSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['coupon_type', 'is_enable', 'activity']
    search_fields = ['coupon_name']

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'receive_coupon']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        queryset = Coupon.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_enable=True)
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CouponCreateUpdateSerializer
        return CouponSerializer

    @action(detail=True, methods=['post'], url_path='receive')
    def receive_coupon(self, request, pk=None):
        """领取优惠券"""
        if not request.user.is_authenticated:
            return Response({'error': '请先登录'}, status=status.HTTP_401_UNAUTHORIZED)

        coupon = self.get_object()
        user = request.user

        # 检查是否已领取
        user_coupon_count = UserCoupon.objects.filter(user=user, coupon=coupon).count()
        if user_coupon_count >= coupon.per_user_limit:
            return Response({'error': '已达到领取上限'}, status=status.HTTP_400_BAD_REQUEST)

        # 检查库存
        if coupon.received_quantity >= coupon.total_quantity:
            return Response({'error': '优惠券已领完'}, status=status.HTTP_400_BAD_REQUEST)

        # 领取优惠券
        start_time = timezone.now()
        end_time = start_time + timedelta(days=coupon.valid_days)

        UserCoupon.objects.create(
            user=user,
            coupon=coupon,
            start_time=start_time,
            end_time=end_time
        )

        coupon.received_quantity += 1
        coupon.save()

        return Response({'message': '领取成功'})


class UserCouponViewSet(viewsets.ReadOnlyModelViewSet):
    """用户优惠券视图集"""
    serializer_class = UserCouponSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserCoupon.objects.filter(user=self.request.user)
