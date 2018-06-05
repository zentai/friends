from flask import Flask, request
from flask_restful import Resource, Api
import json

app = Flask(__name__)
api = Api(app)

friendship = {}

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

api.add_resource(NewFriend, '/new_friends')
api.add_resource(RetrivalFriends, '/friends_list')

if __name__ == '__main__':
    app.run(debug=True)