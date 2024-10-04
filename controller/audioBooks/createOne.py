from flask import request, jsonify
from flask_apispec import MethodResource, marshal_with, doc, use_kwargs
from helper import response_message, Auth, RequestResponse, RequestPost
from model import Audiobook, db
import datetime

from middleware import TokenRequired

class CreateAudiobookRequestPost(RequestPost):
    fields_ = RequestPost.fields_
    title = fields_.Str(required=True, description="Title of the audiobook")
    author = fields_.Str(required=True, description="Author of the audiobook")
    description = fields_.Str(required=False, description="Description of the audiobook")
    cover_image_url = fields_.Str(required=False, description="Cover image URL of the audiobook")

class create_audiobook(MethodResource):

    @doc(description='Create new audiobook')
    @use_kwargs(CreateAudiobookRequestPost, location='json')
    @marshal_with(RequestResponse)
    @TokenRequired 
    def post(self, current_user, **kwargs):
        try:
            
            title = kwargs.get('title')
            author = kwargs.get('author')
            new_audiobook = Audiobook(
                title=title,
                author=author,
                description=kwargs.get('description', ''),
                cover_image_url=kwargs.get('cover_image_url', '')
            )
            
            db.session.add(new_audiobook)
            db.session.commit()

            return response_message(201, 'success', 'Audiobook created successfully.')

        except Exception as e:
            return response_message(500, 'fail', f'An error occurred: {e}')

