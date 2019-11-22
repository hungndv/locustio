import os
import random
import sys
import threading
import uuid
sys.path.append(os.getcwd())
import common.auth

from locust import HttpLocust, TaskSet, task, events
from locust.exception import StopLocust
from locust.main import runners
from bs4 import BeautifulSoup

threadLock = threading.Lock()
global_req_counter = 0
success_req_max = 300

proxies = {
  'http': 'http://10.9.0.49:3128',
  'https': 'http://10.9.0.49:3128',
}

class UserBehavior(TaskSet):
    def setup(self):
        print("TaskSet setup")

    def teardown(self):
        print("TaskSet teardown")

    def on_start(self):
        print("TaskSet on_start")

    def on_stop(self):
        print("TaskSet on_stop")

    @task
    def login(self):
        print("UserBehavior login")
        #raise Exception('EXCEPTION')

        with threadLock:
            global global_req_counter
            global_req_counter += 1
            print("global_counter[{}]".format(global_req_counter))
            if global_req_counter >= success_req_max:
                runners.locust_runner.quit()
        pass

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    #wait_time = random.randint(1, 2)
    userId = uuid.uuid4()

    def __init__(self):
        super(WebsiteUser, self).__init__()
        events.locust_error += self.hook_locust_error

    def hook_locust_error(self, locust_instance, exception, tb):
        print("hook_locust_error")
        runners.locust_runner.quit()
        pass

    def setup(self):
        print("HttpLocust setup userId[{}]".format(self.userId))

    def teardown(self):
        print("HttpLocust teardown userId[{}]".format(self.userId))
        if global_req_counter >= success_req_max:
            print("TEST PASS")
        else:
            print("TEST FAILED - need success_reqs[{}]".format(success_req_max))
