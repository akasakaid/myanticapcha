import requests
import time


class anticaptcha:
    def __init__(self, key):
        self.key = key
        self.uritask = 'https://api.anti-captcha.com/createTask'
        self.urires = 'https://api.anti-captcha.com/getTaskResult'
        self.headers = {
            'accept': 'application/json',
            'content-type': 'application/json'
        }

    def reqtask(self, websiteURL, websiteKEY):
        data = {
            "clientKey": self.key,
            "task":
            {
                "type": "RecaptchaV2TaskProxyless",
                "websiteURL": websiteURL,
                "websiteKey": websiteKEY
            },
            "softId": 0
        }
        req = requests.post(self.uritask, json=data, headers=self.headers)
        if req.json()['errorId'] == 0:
            taskID = req.json()['taskId']
            while True:
                data = {
                    "clientKey": self.key,
                    "taskId": taskID
                }
                req = requests.post(self.urires, json=data,
                                    headers=self.headers)
                if req.json()['errorId'] == 0 and req.json()['status'] == 'ready':
                    return req.json()['solution']['gRecaptchaResponse']
                elif req.json()['status'] == 'processing':
                    time.sleep(5)
                    continue
                elif req.json()['errorId'] != 0:
                    print(req.text)
                    exit()
