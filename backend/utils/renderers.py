from rest_framework.renderers import JSONRenderer
import json as py_json


class UTF8JSONRenderer(JSONRenderer):
    """
    自定义 JSON 渲染器，确保中文不被转义
    """
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        使用标准库 json.dumps 并设置 ensure_ascii=False
        """
        if data is None:
            return b''

        # 使用 Python 标准库的 json.dumps
        ret = py_json.dumps(data, ensure_ascii=False)

        # 返回 UTF-8 编码的字节
        return ret.encode(self.charset)
