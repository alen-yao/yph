"""
短信服务工具类 - 阿里云短信服务封装
"""
import random
import logging
from django.core.cache import cache
from django.conf import settings

logger = logging.getLogger(__name__)


class SMSService:
    """短信验证码服务"""

    # 验证码过期时间（秒）
    CODE_EXPIRE_TIME = 300  # 5分钟

    # 验证码发送频率限制（秒）
    SEND_INTERVAL = 60  # 1分钟

    @staticmethod
    def generate_code(length=6):
        """生成随机验证码"""
        return ''.join([str(random.randint(0, 9)) for _ in range(length)])

    @staticmethod
    def get_cache_key(mobile, code_type='login'):
        """获取缓存key"""
        return f'sms:{code_type}:{mobile}'

    @staticmethod
    def get_send_interval_key(mobile):
        """获取发送间隔缓存key"""
        return f'sms:interval:{mobile}'

    @classmethod
    def can_send(cls, mobile):
        """检查是否可以发送验证码（频率限制）"""
        interval_key = cls.get_send_interval_key(mobile)
        return cache.get(interval_key) is None

    @classmethod
    def send_code(cls, mobile, code_type='login'):
        """
        发送短信验证码

        Args:
            mobile: 手机号
            code_type: 验证码类型 (login: 登录, register: 注册, reset: 重置密码)

        Returns:
            tuple: (success: bool, message: str, code: str)
        """
        # 检查发送频率
        if not cls.can_send(mobile):
            return False, '发送过于频繁，请稍后再试', None

        # 生成验证码
        code = cls.generate_code()

        # 保存到Redis
        cache_key = cls.get_cache_key(mobile, code_type)
        cache.set(cache_key, code, cls.CODE_EXPIRE_TIME)

        # 设置发送间隔
        interval_key = cls.get_send_interval_key(mobile)
        cache.set(interval_key, '1', cls.SEND_INTERVAL)

        # 发送短信
        try:
            success = cls._send_aliyun_sms(mobile, code, code_type)
            if success:
                logger.info(f'短信验证码发送成功: {mobile}, 类型: {code_type}')
                return True, '验证码已发送', code
            else:
                logger.error(f'短信验证码发送失败: {mobile}')
                return False, '短信发送失败，请稍后重试', None
        except Exception as e:
            logger.error(f'短信发送异常: {mobile}, 错误: {str(e)}')
            return False, '短信发送异常', None

    @classmethod
    def verify_code(cls, mobile, code, code_type='login'):
        """
        验证短信验证码

        Args:
            mobile: 手机号
            code: 验证码
            code_type: 验证码类型

        Returns:
            bool: 验证是否成功
        """
        cache_key = cls.get_cache_key(mobile, code_type)
        cached_code = cache.get(cache_key)

        if cached_code is None:
            return False

        if cached_code == code:
            # 验证成功后删除验证码
            cache.delete(cache_key)
            return True

        return False

    @staticmethod
    def _send_aliyun_sms(mobile, code, code_type):
        """
        发送阿里云短信

        配置项（在settings.py中配置）：
        ALIYUN_SMS = {
            'ACCESS_KEY_ID': 'your_access_key_id',
            'ACCESS_KEY_SECRET': 'your_access_key_secret',
            'SIGN_NAME': '你的签名',
            'TEMPLATE_CODE': {
                'login': 'SMS_XXXXX',  # 登录模板
                'register': 'SMS_XXXXX',  # 注册模板
                'reset': 'SMS_XXXXX',  # 重置密码模板
            }
        }
        """
        # 开发环境：直接返回成功，打印验证码
        if settings.DEBUG:
            logger.info(f'[开发环境] 手机号: {mobile}, 验证码: {code}, 类型: {code_type}')
            print(f'\n========== 短信验证码 ==========')
            print(f'手机号: {mobile}')
            print(f'验证码: {code}')
            print(f'类型: {code_type}')
            print(f'有效期: 5分钟')
            print(f'================================\n')
            return True

        # 生产环境：调用阿里云SDK
        try:
            from aliyunsdkcore.client import AcsClient
            from aliyunsdkcore.request import CommonRequest

            sms_config = getattr(settings, 'ALIYUN_SMS', {})

            if not sms_config:
                logger.warning('阿里云短信配置未设置，跳过发送')
                return True

            client = AcsClient(
                sms_config['ACCESS_KEY_ID'],
                sms_config['ACCESS_KEY_SECRET'],
                'cn-hangzhou'
            )

            request = CommonRequest()
            request.set_accept_format('json')
            request.set_domain('dysmsapi.aliyuncs.com')
            request.set_method('POST')
            request.set_protocol_type('https')
            request.set_version('2017-05-25')
            request.set_action_name('SendSms')

            request.add_query_param('PhoneNumbers', mobile)
            request.add_query_param('SignName', sms_config['SIGN_NAME'])
            request.add_query_param('TemplateCode', sms_config['TEMPLATE_CODE'].get(code_type))
            request.add_query_param('TemplateParam', f'{{"code":"{code}"}}')

            response = client.do_action_with_exception(request)
            result = eval(response)

            return result.get('Code') == 'OK'

        except ImportError:
            logger.warning('阿里云SDK未安装，请执行: pip install aliyun-python-sdk-core')
            return False
        except Exception as e:
            logger.error(f'阿里云短信发送异常: {str(e)}')
            return False


class WeChatService:
    """微信登录服务"""

    @staticmethod
    def get_openid_by_code(code, app_type='miniprogram'):
        """
        通过code获取微信openid

        Args:
            code: 微信授权code
            app_type: 应用类型 (miniprogram: 小程序, h5: 公众号)

        Returns:
            dict: {'openid': 'xxx', 'unionid': 'xxx', 'session_key': 'xxx'} or None
        """
        try:
            import requests

            wechat_config = getattr(settings, 'WECHAT', {}).get(app_type, {})

            if not wechat_config:
                logger.error(f'微信配置未设置: {app_type}')
                return None

            # 小程序登录
            if app_type == 'miniprogram':
                url = 'https://api.weixin.qq.com/sns/jscode2session'
                params = {
                    'appid': wechat_config['APP_ID'],
                    'secret': wechat_config['APP_SECRET'],
                    'js_code': code,
                    'grant_type': 'authorization_code'
                }
            # 公众号登录（H5）
            else:
                url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
                params = {
                    'appid': wechat_config['APP_ID'],
                    'secret': wechat_config['APP_SECRET'],
                    'code': code,
                    'grant_type': 'authorization_code'
                }

            response = requests.get(url, params=params, timeout=10)
            result = response.json()

            if 'errcode' in result:
                logger.error(f'微信登录失败: {result}')
                return None

            return {
                'openid': result.get('openid'),
                'unionid': result.get('unionid'),
                'session_key': result.get('session_key'),
                'access_token': result.get('access_token')
            }

        except Exception as e:
            logger.error(f'微信登录异常: {str(e)}')
            return None
