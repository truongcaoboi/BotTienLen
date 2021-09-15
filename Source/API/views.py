from flask import Flask
from flask_restful import Api, Resource, reqparse, request
from logic.TienLenGame import TienLenGame
from logic.NetworkPPO import Agent
import json

app = Flask(__name__)
api = Api(app)

env_game = TienLenGame()
action_space_n = 8192
input_dim = (746,)
agent = Agent(input_dims=input_dim, n_actions=action_space_n)
agent.load_models()

# argument parsing
parser = reqparse.RequestParser()
parser.add_argument('query')

class PredictBotTienLen(Resource):
    def post(self):
        data_revc = json.loads(request.data)
        env_game.set_info_current(data_revc)
        input_network = env_game.create_input_network()
        action_ava = env_game.create_action_availabel()
        action_ex, a,b,c = agent.choose_action(input_network, action_ava)
        data_send = {}
        cardIds = env_game.get_cardids(action_ex)
        data_send["action"] = cardIds
        return data_send, 200

api.add_resource(PredictBotTienLen, '/api/bottienlen/getaction')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)

# @api_view(["POST"])
# def get_action_bot(request):
#     data_revc = request.data
#     env_game.set_info_current(data_revc)
#     input_network = env_game.create_input_network()
#     action_ava = env_game.create_action_availabel()
#     action_ex, a,b,c = agent.choose_action(input_network, action_ava)
#     data_send = {}
#     cardIds = env_game.get_cardids(action_ex)
#     data_send["action"] = cardIds
#     return JsonResponse(data_send, safe=False)