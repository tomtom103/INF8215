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
import random

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
        print("player:", player)
        print("time left:", time_left if time_left else '+inf')
        board = dict_to_board(percepts)

        next_action = self.negamax(board, None, player, 4, -math.inf, math.inf)[1]

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
    ):
        if depth == 0 or board.is_finished():
            return (self.heuristic(board, player, action, depth), action)
        
        actions = list(board.get_actions())

        v_star = -math.inf
        m_star = actions[0]

        for action in actions:
            move_alpha = -self.negamax(board.clone().play_action(action), action, -player, depth - 1, -beta, -alpha)[0]

            if v_star < move_alpha:
                v_star = move_alpha
                m_star = action

            if alpha < move_alpha:
                alpha = move_alpha
                if alpha >= beta:
                    break

        return (v_star, m_star)

    def heuristic(
        self,
        board: Board,
        player: int,
        action: Action,
        depth: int,
    ) -> int:
        score = 0

        #Get the score for the board
        score = board.get_score()

        clone = board.clone()
        x, y, dx, dy = action
        origin, dest = clone.m[x][y], clone.m[dx][dy]

        #Get score for making a tower
        score += self._compute_tower_score(origin,dest,player)

        #making pairs when possible
        score += self._make_pairs(origin,dest,player)

        #stack opps pairs
        score += self._stack_pairs(origin,dest,player)

        # Depth represents depth left to recurse into
        # The smaller it is, the deeper we are.
        # We add a 0.001 bonus to signify that higher score
        # in less turns is more valuable
        score *= (1 + 0.001 * depth)

        return score * player
        

    def _compute_tower_score(self, origin: int, dest: int, player: int) -> int:        
        score = 0

        #1v4
        if origin * dest == -4 and origin == player:
            return 160
        # Complete our own tower if possible (save our own tower) 
        elif origin * dest == 4 and origin == player:
            return 150
        
        #4v1
        if origin * dest == -4 and origin == 4*player:
            return 160
        # Complete our own tower if possible (save our own tower) 
        elif origin * dest == 4 and origin == 4*player:
            return 150

        # 2v3
        if origin * dest == -6 and origin == 2*player:
            return 140
        elif origin * dest == 6 and origin == 2*player :
            return 135

        # 3v2
        if origin * dest == -6 and origin == 3*player:
            return 140
        elif origin * dest == 6 and origin == 3*player :
            return 135

        return score

    def _make_pairs(self, origin: int, dest: int, player: int) :
        score = 0

        #randomly choose between making our pairs or opponents pairs
        p = random.random()

        if p >=0.9 and (origin*dest == 1 and origin == player) : # our pairs
            score += 20
        elif p <= 0.85 and (origin*dest == 1 and origin != player): #opps pairs
            score += 20
        
        return score

    def _stack_pairs(self, origin: int, dest: int, player: int) :
        score = 0

        if  (origin*dest == 4 and origin == -2*player) : 
            score += 15
        
        return score

if __name__ == "__main__":
    agent_main(NegaMaxAgent())