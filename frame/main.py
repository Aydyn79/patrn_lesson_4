from quopri import decodestring

from frame.requests import Post, Get
from patterns.create_pattern import Logger

log = Logger()

class PageNotFound:
    def __call__(self, request):
        return 'Oops, something went wrong.', 'Check if the address is spelled correctly'


class Framework:

    def __init__(self, routes_obj, fronts_obj):
        self.routes = routes_obj
        self.fronts = fronts_obj

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            # конвертируем значения словаря в байты,
            # попутно заменяя знаки
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data

    def __call__(self, env, response):
        # получаем ссылку
        path = env['PATH_INFO']
        # добавляем в конец ссылки слэш, если отсутствует
        path += '/' if path[len(path)-1] != '/' else ''
        request = {}
        # получаем метод запроса
        method_request = env['REQUEST_METHOD']
        # начинаем наполнять словарь запроса данными
        request['method'] = method_request
        if method_request == 'POST':
            data = Post().get_request_params(env)
            request['data'] = Framework.decode_value(data)
            print(f'Пришли данные с формы на странице Contact us: {Framework.decode_value(data)}')
        if method_request == 'GET':
            request_params = Get().get_request_params(env)
            request['request_params'] = Framework.decode_value(request_params)
            print(f'Пришли параметры GET-запроса:'
                  f' {Framework.decode_value(request_params)}')

        # если такой путь существует
        # отработка паттерна page controller
        if path in self.routes:
            view = self.routes[path]
        else:
            view = PageNotFound()

        # наполняем словарь request
        # результатами жизнедеятельности
        # функций add_date, add_key из модуля urls.py
        for item in self.fronts:
            item(request)
        # запуск контроллера с передачей объекта request
        # print(request)
        code, body = view(request)
        response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

