import json

from flask import Response
from flask_restful import Resource


class APIStatus(Resource):
    def get(self):
        """API Status"""
        return Response(json.dumps({'success': True}), status=200,
                        mimetype='application/json')
