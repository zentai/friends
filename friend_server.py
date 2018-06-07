from flask import Flask, request
from flask_restful import Resource, Api
import json

app = Flask(__name__)
api = Api(app)

friendship = {}
subscribe = {}
blacklist = {}

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

        if email not in friendship:
            return error(103, "email %s not registered" % email)

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
            if email not in friendship:
                return error(107, "email %s not registered" % email)

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

        if target not in friendship:
            return error(105, "subscribe target %s not registered" % target)

        if requestor not in friendship:
            return error(106, "subscribe requestor %s not registered" % requestor)


        if target not in subscribe:
            subscribe[target] = set()
        subscribe[target].update(requestor)

        return success()


class Block(Resource):
    def post(self):
        query = request.get_json(force=True)
        requestor = query.get("requestor", None)
        target = query.get("target", None)

        if not requestor or not target:
            return error(104, "please provided both requestor and target email")

        if requestor not in friendship:
            return error(106, "subscribe requestor %s not registered" % requestor)

        if requestor not in blacklist:
            blacklist[requestor] = set()

        blacklist[requestor].update([target])
        return success()


api.add_resource(NewFriend, '/new_friends')
api.add_resource(RetrivalFriends, '/friends_list')
api.add_resource(CommonFriends, '/common_friends')
api.add_resource(Subscribe, '/subscribe')
api.add_resource(Block, '/block')

if __name__ == '__main__':
    app.run(debug=True)