from flask import jsonify
from flask_apispec import MethodResource, marshal_with, doc
from helper import response_message, Auth, RequestResponse
from model import Audiobook, Vote, db

from middleware import TokenRequired

class AudiobooksListAPI(MethodResource):

    @doc(description='Get all audiobooks and check if the user has voted on them.')
    @marshal_with(RequestResponse)
    @TokenRequired  # Assuming this decorator returns a dictionary for current_user
    def get(self, auth):
        try:
            # Access the user ID correctly, assuming current_user is a dict
            user_id = auth['resp']['sub']['data']['username']

            # Fetch all audiobooks from the database
            audiobooks = Audiobook.query.all()

            # Prepare a list to store audiobook data along with vote information
            audiobooks_data = []

            for audiobook in audiobooks:
                # Check if the current user has voted for this audiobook
                has_voted = Vote.query.filter_by(user_id=user_id, audiobook_id=audiobook.id).first() is not None

                # Append audiobook information and vote status
                audiobooks_data.append({
                    'id': audiobook.id,
                    'title': audiobook.title,
                    'author': audiobook.author,
                    'description': audiobook.description,
                    'cover_image_url': audiobook.cover_image_url,
                    'published_on': audiobook.published_on.strftime('%Y-%m-%d'),
                    'vote_count': audiobook.get_vote_count(),
                    'has_voted': has_voted
                })

            # Return response with the list of audiobooks
            return response_message(200, 'success', 'Audiobooks retrieved successfully.', audiobooks_data)

        except Exception as e:
            return response_message(500, 'fail', f'An error occurred: {e}')
