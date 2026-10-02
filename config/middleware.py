from django.http import HttpResponsePermanentRedirect


class WWWRedirectMiddleware:
    """Permanently redirect the www subdomain to the apex domain.

    theroutineparent.com is the canonical host used in every canonical
    tag, Open Graph tag, and email footer. Without this, Cloudflare/Railway
    serve www.theroutineparent.com and theroutineparent.com as two live,
    identical copies of the site with no single canonical host — a
    duplicate content issue for search engines.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host()
        if host.startswith("www."):
            apex_host = host[len("www."):]
            redirect_url = f"{request.scheme}://{apex_host}{request.get_full_path()}"
            return HttpResponsePermanentRedirect(redirect_url)
        return self.get_response(request)
