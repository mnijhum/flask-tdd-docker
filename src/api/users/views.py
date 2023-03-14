from flask import Blueprint, request
from flask_restx import Namespace, Resource, fields

from src import db
from src.api.users.crud import (add_user, delete_user, get_all_users,
                                get_user_by_email, get_user_by_id, update_user)
from src.api.users.models import User

users_namespace = Namespace("users")

user = users_namespace.model(
    "User",
    {
        "id": fields.Integer(readOnly=True),
        "username": fields.String(required=True),
        "email": fields.String(required=True),
        "created_date": fields.DateTime,
    },
)


class UsersList(Resource):
    @users_namespace.expect(user, validate=True)
    @users_namespace.response(201, "<user_email> was added!")
    @users_namespace.response(400, "Sorry, The email already exists.")
    def post(self):
        post_data = request.get_json()
        username = post_data.get("username")
        email = post_data.get("email")

        resposne_object = {}

        user = get_user_by_email(email)
        if user:
            resposne_object["message"] = "Sorry. The email already exists."
            return resposne_object, 400

        add_user(username, email)

        resposne_object["message"] = f"{email} was added!"
        return resposne_object, 201

    @users_namespace.marshal_with(user, as_list=True)
    def get(self):
        """Returns all users."""
        return get_all_users(), 200


class Users(Resource):
    @users_namespace.marshal_with(user)
    @users_namespace.response(200, "Success")
    @users_namespace.response(404, "User <user_id> does not exist")
    def get(self, user_id):
        user = get_user_by_id(user_id)
        if not user:
            users_namespace.abort(404, f"User {user_id} does not exist")
        return user, 200

    @users_namespace.expect(user, validate=True)
    @users_namespace.response(200, "<user_id> was updated!")
    @users_namespace.response(400, "Sorry, That email already exists")
    @users_namespace.response(404, "User <user_id> does not exist")
    def put(self, user_id):
        post_data = request.get_json()
        username = post_data.get("username")
        email = post_data.get("email")

        response_object = {}

        user = get_user_by_id(user_id)

        if not user:
            users_namespace.abort(404, f"User {user_id} does not exist")

        if get_user_by_email(email):
            response_object["message"] = "Sorry. The email already exists."
            return response_object, 400

        update_user(user, username, email)

        response_object["message"] = f"{user.id} was updated!"
        return response_object, 200

    @users_namespace.response(200, "<user_id> was removed!")
    @users_namespace.response(404, "User <user_id> does not exist")
    def delete(self, user_id):
        response_object = {}
        user = get_user_by_id(user_id)

        if not user:
            users_namespace.abort(404, f"User {user_id} does not exist")
        delete_user(user)

        response_object["message"] = f"{user.email} was removed!"
        return response_object, 200


users_namespace.add_resource(UsersList, "")
users_namespace.add_resource(Users, "/<int:user_id>")
