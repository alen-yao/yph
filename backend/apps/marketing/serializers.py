"""营销模块序列化器"""
from rest_framework import serializers
from .models import ActivityBase, Coupon, UserCoupon


class ActivitySerializer(serializers.ModelSerializer):
    activity_type_display = serializers.CharField(source='get_activity_type_display', read_only=True)
    activity_state_display = serializers.CharField(source='get_activity_state_display', read_only=True)

    class Meta:
        model = ActivityBase
        fields = '__all__'


class ActivityCreateUpdateSerializer(serializers.ModelSerializer):
    """活动创建更新序列化器"""

    class Meta:
        model = ActivityBase
        fields = ['activity_name', 'activity_type', 'activity_state', 'start_time',
                  'end_time', 'activity_desc', 'is_enable']

    def validate(self, attrs):
        if attrs.get('end_time') and attrs.get('start_time'):
            if attrs['end_time'] <= attrs['start_time']:
                raise serializers.ValidationError('结束时间必须晚于开始时间')
        return attrs


class CouponSerializer(serializers.ModelSerializer):
    coupon_type_display = serializers.CharField(source='get_coupon_type_display', read_only=True)
    activity_name = serializers.CharField(source='activity.activity_name', read_only=True)

    class Meta:
        model = Coupon
        fields = '__all__'


class CouponCreateUpdateSerializer(serializers.ModelSerializer):
    """优惠券创建更新序列化器"""

    class Meta:
        model = Coupon
        fields = ['activity', 'coupon_name', 'coupon_type', 'coupon_price',
                  'min_amount', 'total_quantity', 'per_user_limit', 'valid_days', 'is_enable']

    def validate_coupon_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('优惠金额必须大于0')
        return value

    def validate_total_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError('总量必须大于0')
        return value


class UserCouponSerializer(serializers.ModelSerializer):
    coupon_info = CouponSerializer(source='coupon', read_only=True)

    class Meta:
        model = UserCoupon
        fields = '__all__'
