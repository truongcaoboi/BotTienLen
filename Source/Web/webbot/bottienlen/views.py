from django.shortcuts import render

# Create your views here.
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from .logic.TienLenGame import TienLenGame
from .logic.NetworkPPO import Agent

from rest_framework.decorators import api_view

env_game = TienLenGame()
action_space_n = 8192
input_dim = (746,)
agent = Agent(input_dims=input_dim, n_actions=action_space_n)
agent.load_models()

@api_view(["POST"])
def get_action_bot(request):
    data_revc = request.data
    env_game.set_info_current(data_revc)
    input_network = env_game.create_input_network()
    action_ava = env_game.create_action_availabel()
    action_ex, a,b,c = agent.choose_action(input_network, action_ava)
    data_send = {}
    cardIds = env_game.get_cardids(action_ex)
    data_send["action"] = cardIds
    return JsonResponse(data_send, safe=False)