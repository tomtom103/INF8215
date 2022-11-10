#!/usr/bin/env python3
"""
Avalam agent.
Copyright (C) 2022, <<<<<<<<<<< YOUR NAMES HERE >>>>>>>>>>>
Polytechnique Montréal

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <http://www.gnu.org/licenses/>.

"""
import math
from avalam import *
from typing import Callable, Tuple, List, Optional
import numpy as np

Action = Tuple[int, int, int, int]

class NegaMaxAgent(Agent):

    """Agent implementing a basic min-max algorithm."""

    def initialize(
        self, 
        percepts: List[List[int]], 
        players: List[Agent], 
        time_left: Optional[float] = None
    ) -> None:
        """Begin a new game.
        The computation done here also counts in the time credit.
        Arguments:
        percepts -- the initial board in a form that can be fed to the Board
            constructor.
        players -- sequence of players this agent controls
        time_left -- a float giving the number of seconds left from the time
            credit for this agent (all players taken together). If the game is
            not time-limited, time_left is None.
        """
        pass
    

    def play(
        self, 
        percepts: List[List[int]], 
        player: int, 
        step: int, 
        time_left: Optional[float] = None
    ) -> Action:
        print("time left:", time_left if time_left else '+inf')
        board = dict_to_board(percepts)

        next_action = self.negamax(board, None, player, 5, -math.inf, math.inf, 1)[1]

        print("Action played: ", next_action)
        return next_action

    def negamax(
        self, 
        board: Board,
        action: Optional[Action],
        player: int, 
        depth: int,
        alpha: float, 
        beta: float,
        color: int,
    ):
        if depth == 0 or board.is_finished():
            return (self.heuristic(board, player) * color, action)
        
        value = -math.inf

        for _action in board.get_actions():
            _value, action = self.negamax(board.clone().play_action(_action), _action, player, depth - 1, -beta, -alpha, -color)
            value = max(value, -_value)
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return (value, action)

    def heuristic(
        self,
        board: Board,
        player: int,
    ) -> int:
        return board.get_score() * player

if __name__ == "__main__":
    agent_main(NegaMaxAgent())