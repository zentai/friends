import unittest
import requests
import json
import sys

class TestFlaskApiUsingRequests(unittest.TestCase):
    def test_new_friends(self):
        response = requests.post("http://127.0.0.1:5000/new_friends",
                                 json={"friends": ["andy@example.com",
                                                   "walao81@example.com",
                                                   "MrBean@example.com"] })
        self.assertEqual(response.json(), {"success": True})


    def test_new_friends_with_one_email(self):
        response = requests.post("http://127.0.0.1:5000/new_friends",
                                 json={"friends": ["andy@example.com"] })
        self.assertEqual(response.json(), {"success": False, "code": 101,
                                           "reason": "at lease 2 difference "
                                                     "email to build friendship"})

    def test_new_friends_with_duplicated_email(self):
        response = requests.post("http://127.0.0.1:5000/new_friends",
                                 json={"friends": ["andy@example.com",
                                                   "andy@example.com"] })
        self.assertEqual(response.json(), {"success": False, "code": 101,
                                           "reason": "at lease 2 difference "
                                                     "email to build friendship"})

    def test_friends_list_success(self):
        response = requests.post("http://127.0.0.1:5000/friends_list",
                                 json={"email": "andy@example.com"})
        self.assertEqual(response.json(), {"success": True, "count": 2,
                                           "friends": ["walao81@example.com",
                                                       "MrBean@example.com"]})


    def test_friends_list_without_email(self):
        response = requests.post("http://127.0.0.1:5000/friends_list",
                                 json={})
        self.assertEqual(response.json(), {"success": False, "code": 102,
                                           "reason": "please pass me the email "
                                                     "your are looking for."})


    def test_friends_list_without_register(self):
        no_register_mail = "no_register@gmail.com"
        response = requests.post("http://127.0.0.1:5000/friends_list",
                                 json={"email": no_register_mail})
        self.assertEqual(response.json(), {"success": False, "code": 103,
                                           "reason": "email %s not registered"
                                           % no_register_mail})


    def test_subscribe_without_requestor(self):
        response = requests.post("http://127.0.0.1:5000/subscribe",
                                 json={"target": "MrBean@example.com"})

        self.assertEqual(response.json(), {"success": False, "code": 104,
                                           "reason": "please provided both "
                                           "requestor and target email"})


    def test_subscribe_without_target(self):
        response = requests.post("http://127.0.0.1:5000/subscribe",
                                 json={"requestor": "lisa@example.com"})

        self.assertEqual(response.json(), {"success": False, "code": 104,
                                           "reason": "please provided both "
                                           "requestor and target email"})


    def test_subscribe_non_register_target(self):
        no_register_mail = "no_register@gmail.com"
        response = requests.post("http://127.0.0.1:5000/subscribe",
                                 json={"requestor": "lisa@example.com",
                                       "target": no_register_mail})

        self.assertEqual(response.json(), {"success": False, "code": 105,
                                           "reason": "subscribe target %s not registered"
                                           % no_register_mail})


    def test_subscribe(self):
        no_register_mail = "no_register@gmail.com"
        response = requests.post("http://127.0.0.1:5000/subscribe",
                                 json={"requestor": "lisa@example.com",
                                       "target": "MrBean@example.com"})

        self.assertEqual(response.json(), {"success": True})


if __name__ == "__main__":
    unittest.main()