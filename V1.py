from instagrapi import Client
import time
cl = Client()
cl.login(username=None, password=None)
# while 1 == 1:

    # print(cl.direct_threads(selected_filter="unread"))
print(cl.direct_thread_by_participants(user_ids=[31395037894]))
    # time.sleep(10)

cl.logout()