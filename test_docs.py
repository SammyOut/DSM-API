from flask import Flask
from flasgger import swag_from, Swagger

app = Flask(__name__)


def parameter(name: str, description: str, in_: str = 'json', type_: str = 'str', required: bool = True) -> dict:
    return {
        'name': name,
        'description': description,
        'in': in_,
        'type': type_,
        'required': required
    }


JWT = parameter('Authorization', 'JWT Token', 'header')


@app.route('/signup', methods=['POST'])
@swag_from({
    'tags': ['Account'],
    'description': '회원가입',
    'parameters': [
        parameter('id', '아이디'),
        parameter('password', '비밀번호'),
        parameter('email', '학교이메일')
    ],
    'responses': {
        '201': {'description': '성공'},
        '409': {'description': '실패'}
    }
})
def signup():
    pass


@app.route('/signin', methods=['POST'])
@swag_from({
    'tags': ['Account'],
    'description': '로그인',
    'parameters': [
        parameter('id', '아이디'),
        parameter('password', '비밀번호')
    ],
    'responses': {
        '200': {
            'description': '성공',
            'examples': {
                '': {'accessToken': '<ACCESS TOKEN>'}
            }
        },
        '409': {'description': '실패'}
    }
})
def sign_in():
    pass


@app.route('/app', methods=['GET'])
@swag_from({
    'tags': ['App'],
    'description': '앱 목록 가져오기',
    'parameters': [JWT],
    'responses': {
        '201': {
            'description': '성공',
            'examples': {
                '': {
                    'appId': 212,
                    'owner': '12a8b7d@@'
                }
            }
        },
        '409': {'description': '실패'}
    }
})
def get_app():
    pass


@app.route('/app', methods=['POST'])
@swag_from({
    'tags': ['App'],
    'description': '앱 등록 신청하기',
    'parameters': [
        parameter('appName', '등록할 앱 이름'),
        parameter('services', '이용할 서비스 리스트', type_='list'),
        parameter('appDescription', '등록할 앱 설명'),
        JWT
    ],
    'responses': {
        '201': {'description': '성공'},
        '409': {'description': '실패'}
    }
})
def create_app():
    pass


@app.route('/app/<int:app_id>', methods=['PATCH'])
@swag_from({
    'tags': ['App'],
    'description': 'Client ID, Secret Key 갱신하기',
    'parameters': [
        parameter('app_id', '삭제할 앱 아이디', type_='integer', in_='url'),
        JWT
    ],
    'responses': {
        '201': {
            'description': '성공, client id, secret key 담겨있는 csv 리스폰스'
        },
        '409': {'description': '실패'}
    }
})
def refresh_secret_key(app_id):
    pass


@app.route('/app/<int:app_id>', methods=['DELETE'])
@swag_from({
    'tags': ['App'],
    'description': '앱 삭제하기',
    'parameters': [
        parameter('app_id', '삭제할 앱 아이디', type_='integer', in_='url'),
        JWT
    ],
    'responses': {
        '201': {'description': '삭제 성공'},
        '409': {'description': '실패'}
    }
})
def delete_app(app_id):
    pass


@app.route('/app/<int:app_id>/user', methods=['GET'])
@swag_from({
    'tags': ['App'],
    'description': '앱 사용을 허용한 유저 목록',
    'parameters': [
        parameter('app_id', '삭제할 앱 아이디', type_='integer', in_='url'),
        JWT
    ],
    'responses': {
        '200': {
            'description': '성공',
            'examples': {
                '': {
                    'user_list': [
                        {
                            'userId': '12a8b7d@@',
                            'userName': '인상민',
                            'userNumber': 3214
                        },
                        {
                            'userId': '1325baccd@@',
                            'userName': '???',
                            'userNumber': 1111
                        }
                    ]
                }
            }
        }
    }
})
def get_app_user(app_id: int):
    pass


@app.route('/service', methods=['GET'])
@swag_from({
    'tags': ['Service'],
    'description': '서비스 목록',
    'parameters': [JWT],
    'responses': {
        '201': {
            'description': '성공',
            'examples': {
                'service_list': [
                    {
                        'serviceId': 1234,
                        'serviceName': 'DSM-Auth',
                        'serviceDescription': '학생 로그인 서비스'
                    }
                ]
            }
        },
        '409': {'description': '실패'}
    }
})
def get_service():
    pass


if __name__ == '__main__':

    app.config['SWAGGER'] = {
        'title': 'DSM-API',
        'specs_route': '/docs',
        'uiversion': 3,

        'info': {
            'title': 'DSM-API',
            'version': '1.0',
            'description': ''
        },
        'basePath': '/',
    }
    Swagger().init_app(app=app)
    app.run()
