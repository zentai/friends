from flask import Flask, request
from flask_restful import Resource, Api
import json
import re


app = Flask(__name__)
api = Api(app)

friendship = {}
subscribe = {}
blacklist = {}

def email_verified(email):
    return re.match(r"[\w\.-]+@[\w\.-]+\.\w+", email)

def error(code, reason):
    return { "success": False, "code": code, "reason": reason }

def success():
    return { "success": True }

def is_black_list(user_a, user_b):
    user_a_blacklist = blacklist.get(user_a, [])
    user_b_blacklist = blacklist.get(user_b, [])
    return user_a in user_b_blacklist or user_b in user_a_blacklist

class NewFriend(Resource):
    def post(self):
        query = request.get_json(force=True)
        friends = query.get("friends", [])

        if len(set(friends)) < 2:
            return error(101, "at lease 2 difference email to build friendship")

        for email in friends:
            if not email_verified(email):
                return error(109, "invalid email")

        black_list_friends = []
        for x in range(len(friends)):
            focus = friends[0]
            fset = friendship.get(focus, set())
            white_list_friends = []
            for friend in friends[1:]:
                if is_black_list(focus, friend):
                    black_list_friends.append(friend)
                else:
                    white_list_friends.append(friend)
            fset.update(white_list_friends)
            friendship[focus] = fset
            friends = friends[1:] + friends[:1]

        if len(black_list_friends) != 0:
            return error(107, "blacklist: %s" % black_list_friends)
        return success()


class RetrivalFriends(Resource):
    def post(self):
        query = request.get_json(force=True)
        email = query.get("email", None)

        if not email:
            return error(102, "please pass me the email your are looking for.")

        if not email_verified(email):
            return error(109, "invalid email")

        if email not in friendship:
            friendship[email] = set()
        success_resp = success()
        success_resp["friends"] = list(friendship.get(email))
        success_resp["count"] = len(friendship.get(email))
        return success_resp


class CommonFriends(Resource):
    def post(self):
        query = request.get_json(force=True)
        friends = query.get("friends", [])

        if len(set(friends)) != 2:
            return error(106, "only support 2 difference email looking friendship")

        for email in friends:
            if not email_verified(email):
                return error(109, "invalid email")

            if email not in friendship:
                friendship[email] = set()

        fset_a = friendship.get(friends[0], set())
        fset_b = friendship.get(friends[1], set())
        min_set = fset_a if len(fset_a) < len(fset_b) else fset_b
        max_set = fset_a if len(fset_a) >= len(fset_b) else fset_b

        common_friends = [email for email in min_set if email in max_set]

        success_resp = success()
        success_resp["friends"] = common_friends
        success_resp["count"] = len(common_friends)
        return success_resp


class Subscribe(Resource):
    def post(self):
        query = request.get_json(force=True)
        requestor = query.get("requestor", None)
        target = query.get("target", None)

        if not requestor or not target:
            return error(104, "please provided both requestor and target email")

        if not email_verified(requestor) or not email_verified(target):
            return error(109, "invalid email")

        if target not in friendship:
            friendship[target] = set()

        if requestor not in friendship:
            friendship[requestor] = set()

        if target not in subscribe:
            subscribe[target] = set()
        subscribe[target].update([requestor])

        return success()


class Block(Resource):
    def post(self):
        query = request.get_json(force=True)
        requestor = query.get("requestor", None)
        target = query.get("target", None)

        if not requestor or not target:
            return error(104, "please provided both requestor and target email")

        if not email_verified(requestor) or not email_verified(target):
            return error(109, "invalid email")

        if requestor not in friendship:
            friendship[requestor] = set()

        if requestor not in blacklist:
            blacklist[requestor] = set()

        blacklist[requestor].update([target])
        return success()


class NotifyList(Resource):
    def post(self):
        query = request.get_json(force=True)
        sender = query.get("sender", None)
        text = query.get("text", "")

        if not email_verified(sender):
            return error(109, "invalid email")

        if not sender:
            return error(108, "sender empty")

        notify_list = set()
        notify_list.update(subscribe.get(sender, set()))
        notify_list.update(re.findall(r"[\w\.-]+@[\w\.-]+\.\w+", text))
        notify_list = notify_list.difference(blacklist.get(sender, set()))

        success_resp = success()
        success_resp["recipients"] = list(notify_list)
        return success_resp

api.add_resource(NewFriend, '/new_friends')
api.add_resource(RetrivalFriends, '/friends_list')
api.add_resource(CommonFriends, '/common_friends')
api.add_resource(Subscribe, '/subscribe')
api.add_resource(Block, '/block')
api.add_resource(NotifyList, '/notify_list')

if __name__ == '__main__':
    app.run(debug=True)