from rest_framework.renderers import JSONRenderer


class UTF8JSONRenderer(JSONRenderer):
    """自定义 JSON 渲染器，确保中文正确显示"""
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """重写 render 方法，使用 ensure_ascii=False"""
        if data is None:
            return b''

        ret = self.encoder_class(
            ensure_ascii=False,
            allow_nan=not self.strict,
            indent=self.get_indent(accepted_media_type, renderer_context),
            separators=self.get_separators()
        ).encode(data)

        # 确保返回的是 bytes
        if isinstance(ret, str):
            return ret.encode(self.charset)
        return ret
