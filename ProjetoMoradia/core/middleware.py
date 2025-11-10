from django.shortcuts import redirect

class HttpsOnlyLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        # 🔒 Se for /login e estiver no HTTP → manda pro servidor HTTPS (porta 8001)
        if path.startswith('/login') and not request.is_secure():
            return redirect(f"https://127.0.0.1:8001{request.get_full_path()}")

        # 🌐 Se NÃO for /login e estiver no HTTPS → manda pro servidor HTTP (porta 8000)
        elif not path.startswith('/login') and request.is_secure():
            return redirect(f"http://127.0.0.1:8000{request.get_full_path()}")

        return self.get_response(request)
