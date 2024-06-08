from flask import Flask
from flask_restful import Resource, Api
from yamconway.SimulationHQ import SimulationHQ

app = Flask(__name__)
api = Api(app)
yc = SimulationHQ()


class BoardState(Resource):
    def get(self):
        yc.next_turn()
        return yc.get_network_board()


class GetNetworkBoard(Resource):
    def get(self):
        return yc.get_network_board()


class NextTurn(Resource):
    def get(self):
        yc.next_turn()
        return yc.get_network_board()


class Reset(Resource):
    def get(self):
        global yc
        yc = SimulationHQ()
        return yc.current_board


api.add_resource(GetNetworkBoard, '/networkboardstate')  # Route_1
api.add_resource(BoardState, '/boardstate')  # Route_1
api.add_resource(NextTurn, '/nextturn')  # Route_1
api.add_resource(Reset, '/reset')

if __name__ == '__main__':
    app.run(port='5002')
