from wsgiref.simple_server import make_server

from frame.main import Framework
from urls import routes, fronts


application = Framework(routes, fronts)

with make_server('', 8000, application) as serv:
    print("Сервер запущен на порту 8000...")
    serv.serve_forever()