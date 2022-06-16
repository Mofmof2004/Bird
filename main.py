import requests
from datetime import datetime
import time
import json
import websockets
import asyncio
import hashlib, base64
from websocket import create_connection
# import pyCookieCheat
class insta_requests():
    def __init__(self):
        self.csrf_token = None
        self.session_key = None
        self.user_agent = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
        self.cookies = None
    def log_in(self, username, password):

        link = 'https://www.instagram.com/accounts/login/'
        login_url = 'https://www.instagram.com/accounts/login/ajax/'

        time = int(datetime.now().timestamp())
        response = requests.get(link)
        csrf = response.cookies['csrftoken']
        print(csrf)
        print(response)
        payload = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}',
            'queryParams': {},
            'optIntoOneTap': 'false'
        }

        login_header = {
            "User-Agent": self.user_agent,
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.instagram.com/accounts/login/",
            "x-csrftoken": csrf
        }


        login_response = requests.post(login_url, data=payload, headers=login_header)
        print(login_response)
        json_data = json.loads(login_response.text)
        print(json_data)

        if json_data["authenticated"]:

            print("LOGIN SUCCESSFUL")
            self.cookies = login_response.cookies
            cookie_jar = self.cookies.get_dict()
            print(cookie_jar)
            self.csrf_token = cookie_jar['csrftoken']
            print("CRSF_TOKEN: ", self.csrf_token)
            self.session_id = cookie_jar['sessionid']
            print("SESSION_TOKEN: ", self.session_id)
        else:
            print("ERROR: WRONG USERNAME OR PASSWORD")


    def get_session_key(self):
        return self.session_key

    def get_csrf_token(self):
        return self.csrf_token
    def test(self):
        url = "https://graph.instagram.com/logging_client_events"

        login_header = {
            "User-Agent": self.user_agent,
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.instagram.com/accounts/login/",

        }
        r = requests.post(url, headers=login_header)

    # def websocket_key_generate(self):
    #
    #     h = hashlib.sha1("dGhlIHNhbXBsZSBub25jZQ==258EAFA5-E914-47DA-95CA-C5AB0DC85B11")
    #
    #     print("hexdigest:", h.hexdigest())  # hexadecimal string representation of the digest
    #
    #     print("digest:", h.digest())  # raw binary digest)
    #
    #
    #
    #     return base64.b64encode(h.digest())
    def web_socket(self):
        import websocket
        import _thread
        import time
        import rel

        def on_message(ws, message):
            print('5')
            print(message)

        def on_error(ws, error):
            print(error)

        def on_close(ws, close_status_code, close_msg):
            print("### closed ###")

        def on_open(ws):
            print("Opened connection")
        def on_data(ws, data):
            print(data)


        websocket.enableTrace(True)
        ws = websocket.WebSocketApp("wss://edge-chat.instagram.com/chat",
                                    on_open=on_open,
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close,
                                    on_data = on_data)




        # ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection

        ws.run_forever(ping_interval=70, ping_timeout=10)
        # print(5)
        # ws.send("sdf")



        rel.signal(2, rel.abort)  # Keyboard Interrupt
        rel.dispatch()
        #
        # url = "wss://edge-chat.instagram.com/chat"
        #
        # ws = create_connection(url, header={"User-Agent": self.user_agent})
        # print(ws)
        # # print(ws.recv())
        # # print("Sending 'Hello, World'...")
        # # ws.send("Hello, World")
        # # print("Sent")
        # print("Receiving...")
        # result = ws.recv()
        # print("Received '%s'" % result)
        # ws.close()








instagram = insta_requests()
try:
    print("LOGGING IN...")

    instagram.log_in(None,None)
except KeyError:
    print("ERROR: LOG IN FAILED")
    time.sleep(1)
    print("NEW LOGGING IN ATTEMPT...")
    instagram.log_in(None, None)
print("ok")
instagram.web_socket()

