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
from transposition_table import BoardWithTransposition
from typing import Tuple, List, Optional

LOWERBOUND, EXACT, UPPERBOUND = -1, 0, 1

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
        board.__class__ = BoardWithTransposition

        next_action = self.negamax(board, None, player, 5, -math.inf, math.inf, 1)[1]

        print("Action played: ", next_action)
        return next_action

    def negamax(
        self, 
        board: Board,
        action: Optional[Action],
        player: int, 
        depth: int,
        origDepth: int,
        alpha: float, 
        beta: float,
        color: int,
        tt=None,
    ):
        alphaOrig = alpha

        lookup = None if (tt is None) else tt.lookup(board)

        if lookup is not None:
            # Game has been visited in the past
            if lookup["depth"] >= depth:
                flag, value = lookup["flag"], lookup["value"]
                if flag == EXACT:
                    if depth == origDepth:
                        # TODO: Idk how this works...
                        move = lookup["move"]
                    return value, action
                elif flag == LOWERBOUND:
                    alpha = max(alpha, value)
                elif flag == UPPERBOUND:
                    beta = min(beta, value)

                if alpha >= beta:
                    if depth == origDepth:
                        move = lookup["move"]
                    return value, action

        if depth == 0 or board.is_finished():
            # Depth represents the depth left to recurse into, the smaller
            # it is the deeper we are in the tree.
            # We could probably add 0.001 * depth to signify that victories
            # in less turns have more value than victories in more turns.
            return (self.heuristic(board, player) * color, action)

        if lookup is not None:
            # Put the supposedly best move first in the list
            actions = list(board.get_actions())
            actions.remove(lookup["move"])
            actions = [lookup["move"]] + actions
        else:
            actions = list(board.get_actions())

        state = board
        best_move = actions[0]
        if depth == origDepth:
            # TODO: Assign move to the first action
            move = actions[0]
        
        
        best_value = -math.inf

        for action in actions:
            board = state.clone()
            board.play_action(action)
            value, _ = self.negamax(board, action, player, depth - 1, origDepth, -beta, -alpha, -color, tt)
            value = -value
            if value > best_value:
                best_value = value
                best_move = action
                if depth == origDepth:
                    move = action
            alpha = max(alpha, value)
            if alpha >= beta:
                break

        if tt is not None:
            assert move in actions
            tt.store(
                board,
                depth,
                best_value,
                best_move,
                UPPERBOUND if best_value <= alphaOrig else LOWERBOUND if best_value >= beta else EXACT,
            )

        return (best_value, best_move)

    def heuristic(
        self,
        board: Board,
        player: int,
    ) -> int:
        return board.get_score() * player

if __name__ == "__main__":
    agent_main(NegaMaxAgent())