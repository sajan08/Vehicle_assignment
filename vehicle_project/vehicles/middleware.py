from django.conf import settings
from django.http import HttpResponseForbidden

class IPFilterMiddleware:
    """
    Simple allow-list IP filter middleware.
    If IP_FILTER_ENABLED is True and ALLOWED_IPS is set, deny requests not from allowed IPs.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.enabled = getattr(settings, 'IP_FILTER_ENABLED', False)
        self.allowed_ips = set(getattr(settings, 'ALLOWED_IPS', []))

    def __call__(self, request):
        if self.enabled:
            ip = self._get_client_ip(request)
            if self.allowed_ips and ip not in self.allowed_ips:
                return HttpResponseForbidden("Your IP is not allowed to access this service.")
        return self.get_response(request)

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
