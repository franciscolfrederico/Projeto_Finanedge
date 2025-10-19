from app import app  # importa o Flask app principal
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.wrappers import Request, Response

def handler(request):
    """Função compatível com Vercel (Serverless)"""
    # O Vercel passa a request como objeto semelhante ao WSGI
    @Request.application
    def application(req):
        # Encaminha a requisição para o Flask app
        return app.wsgi_app(req.environ, lambda *a, **k: None)
    
    return application(request)


