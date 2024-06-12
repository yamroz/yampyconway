from flask import Flask
from flask_restful import Resource, Api
from flask import Response, request
from flask_cors import CORS, cross_origin
from yamconway.SimulationHQ import SimulationHQ

app = Flask(__name__)
api = Api(app)
cors = CORS(app)
yc = SimulationHQ()

@app.route('/boardstate',methods=['GET'])
def BoardState():
    response_content='<html><body><div style="font-family: monospace;">'
    response_content+=yc.get_network_board()
    response_content+='</body></html>'
    return Response(response_content,mimetype='text/html')

@app.route('/nextturn',methods=['POST'])
def NextTurn():
    yc.next_turn()
    return Response(f'Turn {yc.step} calculated correctly.', mimetype='text/plain')

@app.route('/reset',methods=['POST'])
def Reset():
    global yc
    rows = request.args.get('rows')
    columns = request.args.get('columns')
    
    if rows and columns:
        yc = SimulationHQ(rows=int(rows), cells_in_row=int(columns))
    else:
        yc = SimulationHQ()
    response_content=f'Simulation restarted with {yc.current_board.cells_in_row} columns'\
    f' and {len(yc.current_board.rows)} rows.'
    return Response(response_content, mimetype='text/plain')

@app.route('/about', methods=['GET'])
def About():
    reponse_content = '{"about": "yamconway server V0.1"}'
    return Response(reponse_content, mimetype='application/json')

if __name__ == '__main__':
    app.run(port='5000', host="0.0.0.0")
