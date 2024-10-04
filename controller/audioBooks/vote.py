from flask import request
from flask_restful import Api, Resource
from flask_apispec import MethodResource, doc
from helper import response_message
from model import db,Vote
from middleware import TokenRequired

class VoteAPI(MethodResource):

    @doc(description='Vote for or unvote an audiobook.')
    @TokenRequired
    def post(self, auth):
        try:
            # Get the audiobook_id from the request body
            data = request.get_json()
            audiobook_id = data.get('audiobook_id')

            # Check if audiobook_id is provided
            if not audiobook_id:
                return response_message(400, 'fail', 'Audiobook ID is required.')

            user_id = auth['resp']['sub']['data']['username']
            
            if not audiobook_id:
                return response_message(400, 'fail', 'user not found')
            # Log the audiobook_id
        

            # Check if the user has already voted for this audiobook
            existing_vote = Vote.query.filter_by(user_id=user_id, audiobook_id=audiobook_id).first()

            if existing_vote:
                # If the vote exists, delete it
                db.session.delete(existing_vote)
                db.session.commit()
                return response_message(200, 'success', 'Vote removed successfully.')
            else:
                # If no vote exists, create a new vote
                new_vote = Vote(user_id=user_id, audiobook_id=audiobook_id)
                db.session.add(new_vote)
                db.session.commit()
                return response_message(201, 'success', 'Vote recorded successfully.')

        except Exception as e:
            return response_message(500, 'fail', f'An error occurred: {e}')
