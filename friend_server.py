from flask import Flask, request
from flask_restful import Resource, Api
import json

app = Flask(__name__)
api = Api(app)

friendship = {}
subscribe = {}

def error(code, reason):
    return { "success": False, "code": code, "reason": reason }

def success():
    return { "success": True }

class NewFriend(Resource):
    def post(self):
        query = request.get_json(force=True)
        friends = query.get("friends", [])

        if len(set(friends)) < 2:
            return error(101, "at lease 2 difference email to build friendship")

        for x in range(len(friends)):
            focus = friends[0]
            fset = friendship.get(focus, set())
            fset.update(friends[1:])
            friendship[focus] = fset
            friends = friends[1:] + friends[:1]
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

        if target not in subscribe:
            subscribe[target] = set()
        subscribe[target].update(requestor)

        return success()


api.add_resource(NewFriend, '/new_friends')
api.add_resource(RetrivalFriends, '/friends_list')
api.add_resource(CommonFriends, '/common_friends')
api.add_resource(Subscribe, '/subscribe')

if __name__ == '__main__':
    app.run(debug=True)