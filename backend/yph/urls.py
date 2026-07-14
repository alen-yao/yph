"""
YPH 电商系统 URL Configuration
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from healthcheck import health_check
from apps.users.views import CustomTokenObtainPairView

# Swagger API文档配置
schema_view = get_schema_view(
    openapi.Info(
        title="YPH 电商系统 API",
        default_version='v1.0',
        description="""
        YPH电商系统API文档

        基于Python Django + DRF开发
        结合Dailyfresh-B2C的简洁架构和ModulithShop的完整业务功能

        主要功能模块:
        - 用户模块: 用户注册、登录、个人信息管理
        - 商品模块: 商品管理、分类、品牌、SKU
        - 店铺模块: 店铺管理、收藏、浏览历史
        - 交易模块: 购物车、订单、退货、物流
        - 营销模块: 优惠券、活动、秒杀、拼团
        - 支付模块: 微信支付、支付宝支付
        """,
        terms_of_service="https://www.yph.com/terms/",
        contact=openapi.Contact(email="contact@yph.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # 管理后台
    path('admin/', admin.site.urls),

    # 健康检查（用于 Docker 健康检查）
    path('api/health/', health_check, name='health_check'),

    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('api/login/', CustomTokenObtainPairView.as_view(), name='api/login'),

    # API文档
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^api/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),

    # API路由
    path('api/v1/users/', include('apps.users.urls')),
    path('api/v1/products/', include('apps.products.urls')),
    path('api/v1/shops/', include('apps.shops.urls')),
    path('api/v1/trade/', include('apps.trade.urls')),
    path('api/v1/marketing/', include('apps.marketing.urls')),
    path('api/v1/payment/', include('apps.payment.urls')),
    path('api/v1/system/', include('apps.system.urls')),
]

# 开发环境下提供媒体文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# 自定义admin站点信息
admin.site.site_header = 'YPH 电商管理系统'
admin.site.site_title = 'YPH 管理后台'
admin.site.index_title = '欢迎使用 YPH 电商管理系统'
