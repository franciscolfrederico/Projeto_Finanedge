# api/index.py
from app import app
from werkzeug.wrappers import Response

def handler(request):
    """
    Adapta a request do Vercel (semelhante a WSGI) para o Flask WSGI app.
    Retorna um werkzeug.wrappers.Response.
    """
    # 'status' e 'headers' serão preenchidos pelo Flask via start_response
    status_holder = {"status": "500 INTERNAL SERVER ERROR"}
    headers_holder = {"headers": []}

    def start_response(status, headers, exc_info=None):
        status_holder["status"] = status
        headers_holder["headers"] = headers

    # Chama o WSGI app do Flask com o environ da request do Vercel
    result_iterable = app.wsgi_app(request.environ, start_response)

    # Concatena o corpo (o Vercel espera um corpo pronto, não um iterável WSGI)
    body = b"".join(result_iterable)
    try:
        status_code = int(status_holder["status"].split(" ", 1)[0])
    except Exception:
        status_code = 500

    return Response(body, status=status_code, headers=headers_holder["headers"])
