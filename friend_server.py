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
        friendship_json = request.get_json(force=True)
        friends = friendship_json.get("friends", [])

        if len(set(friends)) < 2:
            return error(101, "at lease 2 difference email to create friendship")

        for x in range(len(friends)):
            focus = friends[0]
            fset = friendship.get(focus, set())
            fset.update(friends[1:])
            friendship[focus] = fset
            friends = friends[1:] + friends[:1]
        return success()


api.add_resource(NewFriend, '/new_friends')

if __name__ == '__main__':
    app.run(debug=True)