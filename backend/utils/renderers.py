from rest_framework.renderers import JSONRenderer


class UTF8JSONRenderer(JSONRenderer):
    """
    自定义 JSON 渲染器，确保中文不被转义为 Unicode
    """
    charset = 'utf-8'
    ensure_ascii = False
