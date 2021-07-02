import json

from flask import Response
from flask_restful import Resource, reqparse
from werkzeug.exceptions import BadRequest

from app.main.service.hatchways_service import get_tags_based_posts
from app.main.utils.helpers import (
    format_query_param_error,
    sort_list_of_objects
)


class PostsList(Resource):
    def __init__(self):
        self._args = reqparse.RequestParser()
        self._args.add_argument('tags', type=str, required=True, help='Tags parameter is required')
        self._args.add_argument('sortBy', type=str, choices=['id', 'reads', 'likes', 'popularity'],
                                default='id', help='sortBy parameter is invalid')
        self._args.add_argument('direction', type=str, choices=['asc', 'desc'], default='asc',
                                help='direction parameter is invalid')
        super(PostsList, self).__init__()

    def get(self):
        """
            List all posts
        """
        try:
            args = self._args.parse_args()
            tags = args['tags']
            sort_by = args['sortBy']
            direction = args['direction']

            if tags:
                posts_data = get_tags_based_posts(tags)

                # Sort data if requested
                if sort_by:
                    posts_data = sort_list_of_objects(posts_data, sort_by, direction)

                return Response(json.dumps({'posts': posts_data}), status=200,
                                mimetype='application/json')
            else:
                return Response(json.dumps({'error': 'No tag(s) provided'}), status=400,
                                mimetype='application/json')
        except BadRequest as error:
            return Response(json.dumps(format_query_param_error(error)), status=400,
                            mimetype='application/json')
