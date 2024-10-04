import datetime
from flask_apispec import MethodResource, marshal_with, doc, use_kwargs
from helper import response_message, Auth, RequestResponse, RequestPost
from model import User
from controller import bcrypt, db

class LoginRequestPost(RequestPost):
    fields_ = RequestPost.fields_
    email = fields_.Str(required=True, description="Input Field for Email")  # Changed from username to email
    password = fields_.Str(required=True, description="Input Field for Password")

class LoginAPI(MethodResource):

    @doc(
        description='Login Endpoint.',
    )
    @use_kwargs(LoginRequestPost, location='json')
    @marshal_with(RequestResponse)
    def post(self, **kwargs):
        try:
            # Fetch user by email
            user = User.query.filter_by(email=str(kwargs.get('email'))).first()  # Changed from username to email
            
            # Check if user exists and password matches
            if user and bcrypt.check_password_hash(user.password, kwargs.get('password')):
                # Prepare token data
                auth_token_data = {
                    'email': str(user.email),  # Return email in the token
                    'username': str(user.username)  # Optionally include username as well
                }
                auth_token = Auth(data=auth_token_data).EncodeAuthToken()
                
                if auth_token:
                    # Update user's last login time
                    user.last_logged_in = datetime.datetime.now()
                    user.last_logged_out = None
                    db.session.commit()

                    # Prepare the response data
                    data = {
                        'auth_token': auth_token,
                        'username': user.username,  # Include username in the response
                        'email': user.email,
                        'name': user.name,  # Include name; can be None if not provided
                        'referral_code': user.referral_code,  # Assuming this field exists
                        # Add more fields as required
                    }
                    
                    return response_message(200, 'success', 'Successfully logged in.', data)
            else:
                return response_message(404, 'fail', 'User does not exist or email/password mismatch.')
        
        except Exception as e:
            return response_message(500, 'fail', f'An error occurred: {e}')
