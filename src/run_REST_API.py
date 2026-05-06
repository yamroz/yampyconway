from flask import Flask, jsonify
from flask_restful import Resource, Api
from yamconway.SimulationHQ import SimulationHQ
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
api = Api(app)
yc = SimulationHQ()


class BoardState(Resource):
    def get(self):
        try:
            yc.next_turn()
            return yc.get_network_board()
        except Exception as e:
            logger.error(f"Error in BoardState endpoint: {e}", exc_info=True)
            return jsonify({
                'error': 'Failed to advance simulation',
                'message': str(e)
            }), 500


class GetNetworkBoard(Resource):
    def get(self):
        try:
            return yc.get_network_board()
        except Exception as e:
            logger.error(f"Error in GetNetworkBoard endpoint: {e}", exc_info=True)
            return jsonify({
                'error': 'Failed to retrieve board state',
                'message': str(e)
            }), 500


class NextTurn(Resource):
    def get(self):
        try:
            yc.next_turn()
            return yc.get_network_board()
        except Exception as e:
            logger.error(f"Error in NextTurn endpoint: {e}", exc_info=True)
            return jsonify({
                'error': 'Failed to advance simulation',
                'message': str(e)
            }), 500


class Reset(Resource):
    def get(self):
        try:
            global yc
            yc = SimulationHQ()
            return yc.current_board
        except Exception as e:
            logger.error(f"Error in Reset endpoint: {e}", exc_info=True)
            return jsonify({
                'error': 'Failed to reset simulation',
                'message': str(e)
            }), 500


class Version(Resource):
    def get(self):
        try:
            global yc
            return yc.get_version()
        except Exception as e:
            logger.error(f"Error in Version endpoint: {e}", exc_info=True)
            return jsonify({
                'error': 'Failed to get version',
                'message': str(e)
            }), 500


api.add_resource(GetNetworkBoard, '/networkboardstate')  # Route_1
api.add_resource(BoardState, '/boardstate')  # Route_1
api.add_resource(NextTurn, '/nextturn')  # Route_1
api.add_resource(Reset, '/reset')
api.add_resource(Version, '/app_info')

if __name__ == '__main__':
    app.run(port='5002', debug=True)
