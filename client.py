import json
from json import JSONDecodeError
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE_URL = 'http://127.0.0.1:5001'


def parse_response_body(response_body: str):
    if not response_body:
        return {'message': 'Empty response body'}

    try:
        return json.loads(response_body)
    except JSONDecodeError:
        return {'message': response_body}


def send_request(path: str, method: str = 'GET', data: dict | None = None):
    url = f'{BASE_URL}{path}'
    body = None
    headers = {}

    if data is not None:
        body = json.dumps(data).encode('utf-8')
        headers['Content-Type'] = 'application/json'

    request = Request(url, data=body, headers=headers, method=method)

    try:
        with urlopen(request) as response:
            response_body = response.read().decode('utf-8')
            return response.status, parse_response_body(response_body)
    except HTTPError as error:
        response_body = error.read().decode('utf-8')
        return error.code, parse_response_body(response_body)
    except URLError as error:
        return None, {
            'message': f'Cannot connect to API: {error.reason}'
        }


def get_health():
    return send_request('/health')


def get_categories():
    return send_request('/categories')


def get_goods():
    return send_request('/goods')


def create_good(name: str, price: float, category_id: int):
    return send_request(
        '/goods',
        method='POST',
        data={
            'name': name,
            'price': price,
            'category_id': category_id,
        }
    )


def print_response(title: str, response):
    status_code, data = response
    print(title)
    print('Status:', status_code)
    print('Data:', data)
    print()


if __name__ == '__main__':
    print_response('Health', get_health())
    print_response('Categories', get_categories())
    print_response('Goods', get_goods())
