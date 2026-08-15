class UTF8ResponseMiddleware:
    """
    强制所有 HTTP 响应使用 UTF-8 编码
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # 强制设置 Content-Type 为 UTF-8
        if 'application/json' in response.get('Content-Type', ''):
            response['Content-Type'] = 'application/json; charset=utf-8'

        return response
