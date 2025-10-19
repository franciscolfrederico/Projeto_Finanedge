# api/index.py
from app import app  # o objeto Flask no app.py deve se chamar "app"

import sys
def handler(request):
    return {"statusCode": 200, "headers": {"Content-Type": "text/plain"}, "body": sys.version}
