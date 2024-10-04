import datetime
from flask_apispec import MethodResource, marshal_with, doc, use_kwargs
from helper import response_message, Auth, Serializers, RequestResponse, RequestPost
from model import User
from controller import bcrypt, db


class RegisterRequest(RequestPost):
    fields_ = RequestPost.fields_
    username = fields_.Str(required=True, description="Input Field for Username")
    password = fields_.Str(required=True, description="Input Field for Password")
    email = fields_.Str(required=True, description="Input Field for Email")
    name = fields_.Str(required=False, description="Input Field for Name")  # Set required to False


class RegisterAPI(MethodResource):

    @doc(
        description='Register Endpoint.'
    )
    @use_kwargs(RegisterRequest, location='json')
    @marshal_with(RequestResponse)
    def post(self, **kwargs):
        user = User.query.filter_by(username=kwargs.get('username')).first()
        if not user:
            try:
                # Validate and create a new user instance
                user = Serializers(kwargs).ValidatingRegister()

                # Add the new user to the database
                db.session.add(user)
                db.session.commit()

                # Generate authentication token
                auth_token_data = {
                    'username': str(user.username)
                }
                auth_token = Auth(data=auth_token_data).EncodeAuthToken()

                # Optional: Update the user's last logged-in time
                user.last_logged_in = datetime.datetime.now()
                db.session.commit()

                # Prepare the response data
                data = {
                    'auth_token': auth_token,
                    'username': user.username,
                    'email': user.email,
                    'name': user.name,  # This can now be None if not provided
                    'referral_code': user.referral_code  # Assuming this field exists
                }

                return response_message(201, 'success', 'Successfully registered.', data)

            except Exception as e:
                return response_message(401, 'fail', str(e))
        else:
            return response_message(202, 'already_exists', 'User already exists. Please Log in.')
