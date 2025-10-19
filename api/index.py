# api/index.py
from app import app
from werkzeug.wrappers import Request, Response
import traceback

def handler(request):
    """Adapta a request do Vercel para o WSGI do Flask com logs de erro."""
    @Request.application
    def application(req):
        try:
            # Encaminha a requisição para o WSGI do Flask
            return app.wsgi_app(req.environ, lambda *a, **k: None)
        except Exception:
            # LOGA nos logs do Vercel (stdout/stderr)
            traceback.print_exc()
            # (temporário) devolve o stack trace para conseguirmos ver a causa no browser
            return Response(
                "Internal error:\n\n" + traceback.format_exc(),
                status=500,
                content_type="text/plain; charset=utf-8",
            )
    return application(request)


