from django.core.cache import cache
from django.http import HttpResponseForbidden


class IPLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/usuarios/registrar/':  # Aplica apenas no registro
            ip = request.META.get('REMOTE_ADDR')
            cache_key = f"limit_ip_{ip}"
            count = cache.get(cache_key, 0)

            if count >= 70:  # Limite de 3 cadastros por IP por dia
                return HttpResponseForbidden("Limite de cadastros por IP excedido.")

            # Nota: O incremento deve ser feito após a criação do usuário com sucesso
        return self.get_response(request)
