from wsrequests import WsRequests

wsr = WsRequests()

# login django
wsr.get('http://localhost:3000/accounts/login/')
wsr.post(
    'http://localhost:3000/accounts/login/',
    data={
        'username': 'admin',  # Djangoのユーザ名とパスワード
        'password': 'passpass',
        'csrfmiddlewaretoken': wsr.cookies['csrftoken'],
        'next': '/',
    }
)
wsr.connect('ws://localhost:3000/ws/boards/35')
wsr.receive_message()
wsr.disconnect()
