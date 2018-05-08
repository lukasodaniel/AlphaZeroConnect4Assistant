$(document).ready(function() {
	var current_state = {
		to_play : null,
		legal_moves : null,
		game_board : null,
		player1 : null,
		player2 : null,
		to_play_id : null,
		endgame : false
	};
	$('#play-button').click(function() { play_selected_move(); });

	var get_player1 = function() {
		for (var i in game_modes) {
			if ($('#p1' + game_modes[i]).prop('checked')){
				return game_modes[i];
			} 
		}
	};

	var get_player2 = function() {
		for (var i in game_modes) {
			if ($('#p2' + game_modes[i]).prop('checked')){
				return game_modes[i];
			} 
		}
	};

	var play_selected_move = function() {
		var to_play_space =  parseInt($('.selected').attr('id').split('-')[1]);
		var to_send = {
			move: to_play_space,
			current_state: current_state
		};
		$.ajax({
			type: 'POST',
			url: '/play/',
			data: JSON.stringify(to_send),
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			success: function(data) {
				if(data.endgame == 1) {
					current_state.endgame = true;
					current_state.legal_moves = null;
					current_state.to_play = null;
					current_state.to_play_id = null;
					//endgame();
				} else {
					current_state.to_play = data.to_play;
					current_state.legal_moves = data.legal_moves;
				}
				
				current_state.game_board = data.game_board;
				current_state.to_play_id = -current_state.to_play_id;
				$('#play-button').prop('disabled', true);
				$('.selected').removeClass('selected');
				refresh_game_board();

				if(data.endgame == 1) {
					alert("Player " + current_state.to_play.split('r')[1] + " wins");
				}
			}
		});
	}

	var get_computer_move = function() {
		//assumpiton is we know that the comptuer is to play
		$.ajax({
			type: 'POST',
			url: '/get-computer-move/',
			data: JSON.stringify(current_state),
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			success: function(data) {
				if(data.endgame == 1) {
					current_state.endgame = true;
					current_state.legal_moves = null;
					current_state.to_play = null;
					current_state.to_play_id = null;
					//endgame();
				} else {
					current_state.to_play = data.to_play;
					current_state.legal_moves = data.legal_moves;
				}
				
				current_state.game_board = data.game_board;
				current_state.to_play_id = -current_state.to_play_id;
				refresh_game_board();

				if(data.endgame == 1) {
					alert("Player " + current_state.to_play.split('r')[1] + " wins");
				}
			}
		})
	}

	var refresh_game_board = function() {
		$('.legal-move').off();
		$('.legal-move').removeClass('legal-move');
		if(current_state.game_board != null) {
			for (var i in current_state.game_board) {
				if (current_state.game_board[i] == 1) {
					$('#space-'+i).addClass('player1');
				} else if (current_state.game_board[i] == -1) {
					$('#space-'+i).addClass('player2');
				}
			}
		}

		if(current_state.legal_moves != null) {
			for(var i in current_state.legal_moves) {
				//$('#space'+current_state.legal_moves[i]).css('border', '2px solid orange');
				$('#space-'+current_state.legal_moves[i]).addClass('legal-move');
				$('.legal-move').click(function() {
					$('.selected').removeClass('selected');
					$(this).addClass('selected');
					
				});
			}
		}
		if(current_state[current_state['to_play']] == 'computer') {
			get_computer_move();
		} else {
			$('#play-button').prop('disabled', false);
		}
	};

	$("#new-game").click(function() {
		$('.legal-move').off();
		$('.game-space').removeClass('legal-move');
		$('.game-space').removeClass('player1');
		$('.game-space').removeClass('player2');
		current_state.player1 = get_player1();
		current_state.player2 = get_player2();
		current_state.to_play_id = 1;
		$.getJSON('/new-game/'+current_state.player1+'/'+current_state.player2, 
			function(data) {
				current_state.game_board = data.game_board;
				current_state.to_play = data.to_play;
				current_state.legal_moves = data.legal_moves;
				refresh_game_board();
		});
	});

	var game_modes = ['unassisted', 'assisted', 'computer'];
	
});