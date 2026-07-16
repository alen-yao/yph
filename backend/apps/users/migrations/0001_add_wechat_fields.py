# Generated manually - Add wechat login fields to existing User table
from django.db import migrations, models


class Migration(migrations.Migration):

    # 如果是第一个迁移，dependencies可以为空
    # 如果之前有迁移记录，改成实际的依赖
    dependencies = []

    operations = [
        migrations.AddField(
            model_name='user',
            name='wechat_openid',
            field=models.CharField(
                blank=True,
                max_length=100,
                null=True,
                unique=True,
                verbose_name='微信OpenID'
            ),
        ),
        migrations.AddField(
            model_name='user',
            name='wechat_unionid',
            field=models.CharField(
                blank=True,
                max_length=100,
                null=True,
                verbose_name='微信UnionID'
            ),
        ),
    ]
