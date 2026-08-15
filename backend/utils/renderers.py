from rest_framework.renderers import JSONRenderer
from rest_framework.utils import json


class UTF8JSONRenderer(JSONRenderer):
    """
    自定义 JSON 渲染器，使中文不被转义为 Unicode
    设置 ensure_ascii=False 使中文正常显示
    """
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        重写 render 方法，强制使用 ensure_ascii=False
        """
        if data is None:
            return b''

        renderer_context = renderer_context or {}
        indent = self.get_indent(accepted_media_type, renderer_context)

        if indent is None:
            separators = (',', ':')
        else:
            separators = (',', ': ')

        ret = json.dumps(
            data,
            cls=self.encoder_class,
            indent=indent,
            ensure_ascii=False,
            allow_nan=not self.strict,
            separators=separators
        )

        return ret.encode(self.charset)
