
import numpy as np
np.set_printoptions(suppress=True)

from shutil import copyfile
import random



from game import Game, GameState
from agent import Agent
from memory import Memory
from model import Residual_CNN
from funcs import playMatches

import loggers as lg

from settings import run_folder, run_archive_folder
import initialise
import pickle

from settings import run_folder, run_archive_folder
import initialise
import pickle

from bottle import request, response, route, run
from bottle import post, get, put, delete, static_file

import re, json

env = Game()


import config

ai_player_NN = Residual_CNN(config.REG_CONST, 
                            config.LEARNING_RATE, 
                            env.input_shape,   
                            env.action_size, 
                            config.HIDDEN_CNN_LAYERS)
ai_player_network = ai_player_NN.read_path('version0024.h5')
ai_player_NN.model.set_weights(ai_player_network.get_weights())
ai_player = Agent('ai_player', 
                env.state_size, 
                env.action_size, 
                config.MCTS_SIMS, 
                config.CPUCT, 
                ai_player_NN)

@get('/')
def get_home_page():
    return static_file('./website/index.html', root='.')

@get('/js/<filename>')
def get_js_files(filename):
    return static_file(filename, root='./website/js/')

def computer_play(game_state):
    action, _a, _b, _c = ai_player.act(game_state, 1)
    return action

@post('/get-suggestions')
def computer_suggest():
    req = json.load(request.body)
    game_state = req['game_state']
    req['legal_moves'] = ai_player.get_preds(game_state)
    return json.dumps(req)

@post('/play/')
def play():
    req = json.load(request.body)
    print(req)
    state = req['current_state']
    board_array = state['game_board']
    board_array[req['move']] = 1 if state['to_play'] == 'player1' else -1
    to_play_id = -state['to_play_id']
    new_game_state = GameState(board_array, to_play_id)
    to_play = 'player2' if state['to_play'] == 'player1' else 'player1'
    rv = {
        'player1' : state['player1'],
        'player2' : state['player2'],
        'game_board' : new_game_state.board,
        'endgame' : new_game_state.isEndGame,
        'to_play' : to_play,
        'legal_moves' : new_game_state._allowedActions(),
        'to_play_id' : to_play_id
    }
    if rv[to_play] == 'assisted':
        _, preds, moves = ai_player.get_preds(new_game_state)
        print(preds)
        print(list(np.argpartition(preds, -3)[-3:]))
        rv['legal_moves'] = list(np.argpartition(preds, -3)[-3:])
    
    return json.dumps(rv)

@post('/get-computer-move/')
def get_computer_move():
    state = json.load(request.body)
    print(state)
    board_array = state['game_board']
    to_play_id = state['to_play_id']
    current_state = GameState(board_array, to_play_id)
    _, preds, moves = ai_player.get_preds(current_state)
    computer_move = np.argmax(preds)
    board_array[computer_move] = to_play_id
    new_game_state = GameState(board_array, -to_play_id)
    to_play = 'player2' if state['to_play'] == 'player1' else 'player1'
    rv = {
        'player1' : state['player1'],
        'player2' : state['player2'],
        'game_board' : new_game_state.board,
        'endgame' : new_game_state.isEndGame,
        'to_play' : to_play,
        'legal_moves' : new_game_state._allowedActions(),
        'to_play_id' : -to_play_id
    }
    if rv[to_play] == 'assisted':
        _, preds, moves = ai_player.get_preds(new_game_state)
        print(preds)
        print(list(np.argpartition(preds, -3)[-3:]))
        rv['legal_moves'] = list(np.argpartition(preds, -3)[-3:])

    return json.dumps(rv)

@get('/new-game/<player1>/<player2>')
def new_game(player1, player2):
    '''Handles name listing'''
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    new_game_board_array = [
        0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,
        0,0,0,0,0,0,0
    ]
    new_game_state = GameState(new_game_board_array, 1)
    rv = {
        'player1' : player1,
        'player2' : player2,
        'game_board' : new_game_state.board,
        'to_play' : 'player1',
        'legal_moves' : new_game_state._allowedActions()
    }
    if player1 == 'assisted':
        _, preds, moves = ai_player.get_preds(new_game_state)
        rv['legal_moves'] = list(np.argpartition(preds, -3)[-3:])
    return json.dumps(rv)

run(host='localhost', port=8080, debug=True)

