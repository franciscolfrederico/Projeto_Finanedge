# api/index.py
import traceback
from werkzeug.wrappers import Request, Response

def handler(request):
    # 1) Tenta importar o Flask app e captura erros de import (acontecem antes da resposta)
    try:
        from app import app  # precisa existir app.py na raiz com objeto "app"
    except Exception:
        tb = traceback.format_exc()
        print("=== IMPORT_ERROR ===\n", tb, flush=True)  # aparece em /_logs
        return Response(
            "Import error:\n\n" + tb,
            status=500,
            content_type="text/plain; charset=utf-8",
        )

    # 2) Se importou, adapta a request para WSGI e captura erros de execução
    @Request.application
    def application(req):
        try:
            return app.wsgi_app(req.environ, lambda *a, **k: None)
        except Exception:
            tb = traceback.format_exc()
            print("=== RUNTIME_ERROR ===\n", tb, flush=True)
            return Response(
                "Runtime error:\n\n" + tb,
                status=500,
                content_type="text/plain; charset=utf-8",
            )

    return application(request)
