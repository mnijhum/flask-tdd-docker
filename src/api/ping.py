from flask import Blueprint
from flask_restx import Api, Namespace, Resource

ping_namespace = Namespace("ping")


class Ping(Resource):
    def get(self):
        return {"status": "success", "message": "ding dong ping pong!!!!"}


ping_namespace.add_resource(Ping, "")
